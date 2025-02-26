from django.contrib.auth.models import User, Group
from drf_haystack.serializers import HighlighterMixin, HaystackSerializer
from rest_framework import serializers

from api import models
from api import search_indexes

class ManifestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manifest
        fields = ('filename', 'type', 'hash', 'created_at')

class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
            model = models.Document
            fields = (
                'title', 
                'slug', 
                'url',
                'license',
                'desc',
                'license',
                'author',
                'organization',
                'version',
                'created_at',
                'copyright',
                'license_url',)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class MonsterSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    
    img_main = serializers.SerializerMethodField()

    def get_img_main(self, monster):
        request = self.context.get('request')
        domain = str(request.get_host())
        img_url = monster.img_main
        if img_url != None:
            return ('http://{domain}/{path}'.format(domain=domain, path=img_url))
        else:
             return None
            
    class Meta:
        model = models.Monster
        fields = (
            'slug',
            'name',
            'size',
            'type',
            'subtype',
            'group',
            'alignment',
            'armor_class',
            'armor_desc',
            'hit_points',
            'hit_dice',
            'speed',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'strength_save',
            'dexterity_save',
            'constitution_save',
            'intelligence_save',
            'wisdom_save',
            'charisma_save',
            'perception',
            'skills',
            'damage_vulnerabilities',
            'damage_resistances',
            'damage_immunities',
            'condition_immunities',
            'senses',
            'languages',
            'challenge_rating',
            'cr',
            'actions',
            'reactions',
            'legendary_desc',
            'legendary_actions',
            'special_abilities',
            'spell_list',
            'img_main',
            'document__slug',
            'document__title',
            'document__license_url',
        )

class SpellSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Spell
        fields = (
            'slug',
            'name',
            'desc',
            'higher_level',
            'page',
            'range',
            'components',
            'material',
            'ritual',
            'duration',
            'concentration',
            'casting_time',
            'level',
            'level_int',
            'school',
            'dnd_class',
            'archetype',
            'circles',
            'document__slug',
            'document__title',
            'document__license_url',
        )

class BackgroundSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Background
        fields = (
            'name',
            'desc',
            'slug',
            'skill_proficiencies',
            'tool_proficiencies',
            'languages',
            'equipment',
            'feature',
            'feature_desc',
            'suggested_characteristics',
            'document__slug',
            'document__title',
            'document__license_url',
        )

class PlaneSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Plane
        fields = ('slug','name','desc','document__slug', 'document__title')

class SectionSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Section
        fields = (
            'slug',
            'name',
            'desc',
            'document__slug',
            'document__title',
            'document__license_url',
            'parent'
        )

class FeatSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Feat
        fields = (
            'slug',
            'name',
            'desc',
            'prerequisite',
            'document__slug',
            'document__title'
        )

class ConditionSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Condition
        fields = (
            'slug',
            'name',
            'desc',
            'document__slug',
            'document__title'
        )

class SubraceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Subrace
        fields = ('name',
        'slug',
        'desc',
        'asi',
        'traits',
        'asi_desc',
        'document__slug',
        'document__title'
    )


class RaceSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    subraces = SubraceSerializer(many=True,read_only=True)
    class Meta:
        model = models.Race
        fields = (
            'name',
            'slug',
            'desc',
            'asi_desc',
            'asi',
            'age',
            'alignment',
            'size',
            'speed',
            'speed_desc',
            'languages',
            'vision',
            'traits',
            'subraces',
            'document__slug',
            'document__title',
            'document__license_url',
        )

class ArchetypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Archetype
        fields = (
            'name',
            'slug',
            'desc',
            'document__slug',
            'document__title',
            'document__license_url',
        )

class CharClassSerializer(serializers.HyperlinkedModelSerializer):
    archetypes = ArchetypeSerializer(many=True,read_only=True)
    class Meta:
        model = models.CharClass
        fields = (
            'name',
            'slug',
            'desc',
            'hit_dice',
            'hp_at_1st_level',
            'hp_at_higher_levels',
            'prof_armor',
            'prof_weapons',
            'prof_tools',
            'prof_saving_throws',
            'prof_skills',
            'equipment',
            'table',
            'spellcasting_ability',
            'subtypes_name',
            'archetypes',
            'document__slug',
            'document__title',
            'document__license_url',
        )

class MagicItemSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MagicItem
        fields = (
            'slug',
            'name',
            'type',
            'desc',
            'rarity',
            'requires_attunement',
            'document__slug',
            'document__title'
        )

class WeaponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Weapon
        fields = (
            'name',
            'slug',
            'category',
            'document__slug',
            'document__title',
            'document__license_url',
            'cost',
            'damage_dice',
            'damage_type',
            'weight',
            'properties')

class ArmorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Armor
        fields = (
            'name',
            'slug',
            'category',
            'document__slug',
            'document__title',
            'document__license_url',
            'ac_string',
            'strength_requirement',
            'cost',
            'weight',
            'stealth_disadvantage')


class AggregateSerializer(HighlighterMixin, HaystackSerializer):

    class Meta:
        index_classes = [search_indexes.MonsterIndex, 
            search_indexes.SpellIndex, 
            search_indexes.SectionIndex, 
            search_indexes.ConditionIndex, 
            search_indexes.CharClassIndex, 
            search_indexes.RaceIndex,
            search_indexes.MagicItemIndex,]
        fields = ['name',
            'text',
            'route',
            'slug',
            'level',
            'school',
            'dnd_class',
            'ritual',
            'armor_class',
            'hit_points',
            'hit_dice',
            'challenge_rating',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'rarity',
            'type',
            'source',
            'requires_attunement',
            'document_slug',
            'document_title'
        ]
        
