# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from ralph.assets.models.assets import (
    AssetHolder,
    AssetModel,
    BudgetInfo,
    BusinessSegment,
    Category,
    Environment,
    Manufacturer,
    ManufacturerKind,
    ProfitCenter,
    Service,
    ServiceEnvironment
)
from ralph.assets.models.base import BaseObject
from ralph.assets.models.choices import ComponentType, ObjectModelType
from ralph.assets.models.components import (
    ComponentModel,
    Disk,
    Ethernet,
    FibreChannelCard,
    Memory,
    Processor
)
from ralph.assets.models.configuration import (
    ConfigurationClass,
    ConfigurationModule
)


def next_mac(n):
    mac = [0x00, 0x16, 0x3E, n >> 16 & 0xFF, n >> 8 & 0xFF, n & 0xFF]
    return ":".join(map(lambda x: "%02x" % x, mac))


def next_wwn(n):
    # Every WWN produced by this function is a string containing a sequence
    # of 16 hex digits, where the first 10 are fixed ('aabbccddee'), and the
    # the remaining 6 are generated by by bit shifting. So for example:
    # n = 0 gives 'aabbccddee000000',
    # n = 1 gives 'aabbccddee000001',
    # n = 2 gives 'aabbccddee000002',
    # ...
    # n = 32 gives 'aabbccddee000020',
    # ...and so on.
    wwn = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, n >> 16 & 0xFF, n >> 8 & 0xFF, n & 0xFF]
    return "".join(map(lambda x: "%02x" % x, wwn))


class ComponentModelFactory(DjangoModelFactory):
    speed = factory.Iterator(["2700", "2500", "2100"])
    cores = factory.Iterator(["2", "4", "8"])
    size = factory.Iterator(["512", "1024", "2048"])
    type = factory.Iterator(
        [
            ComponentType.processor.id,
            ComponentType.memory.id,
            ComponentType.disk.id,
            ComponentType.ethernet.id,
        ]
    )
    name = FuzzyText()
    family = FuzzyText()

    class Meta:
        model = ComponentModel
        django_get_or_create = ["name", "speed", "cores", "size", "type", "family"]


class BaseObjectFactory(DjangoModelFactory):
    class Meta:
        model = BaseObject


class CategoryFactory(DjangoModelFactory):
    imei_required = True
    show_buyout_date = True
    name = factory.Iterator(
        [
            "Dictaphone",
            "Disk",
            "External disk",
            "External drive",
            "Headphones",
            "Keyboard",
            "Mouse",
            "Pendrive",
            "Notebook",
        ]
    )

    class Meta:
        model = Category
        django_get_or_create = ["name"]


class DataCenterCategoryFactory(DjangoModelFactory):
    imei_required = False
    name = factory.Iterator(
        ["ATS", "Database Machine", "Blade System", "Chassis blade"]
    )

    class Meta:
        model = Category
        django_get_or_create = ["name"]


class AssetHolderFactory(DjangoModelFactory):
    name = factory.Iterator(["Grupa Allegro SP. z o.o.", "Google Inc.", "Dell Inc"])

    class Meta:
        model = AssetHolder
        django_get_or_create = ["name"]


class BudgetInfoFactory(DjangoModelFactory):
    name = factory.Iterator(["Python Team", "Django team", "Redis Team", "PSQL Team"])

    class Meta:
        model = BudgetInfo
        django_get_or_create = ["name"]


class ManufacturerKindFactory(DjangoModelFactory):
    name = factory.Iterator(
        [
            "kind-a",
            "kind-b",
            "kind-c",
        ]
    )

    class Meta:
        model = ManufacturerKind
        django_get_or_create = ["name"]


class ManufacturerFactory(DjangoModelFactory):
    name = factory.Iterator(
        [
            "Dell",
            "Apple",
            "Samsung",
            "Adobe",
            "Asus",
            "Atlassian",
            "BenQ",
            "Belkin",
            "Bosh",
            "Brother",
            "Foxconn",
            "Fujitsu",
            "HUAWEI",
            "HTC",
        ]
    )

    class Meta:
        model = Manufacturer
        django_get_or_create = ["name"]


class BackOfficeAssetModelFactory(DjangoModelFactory):
    name = factory.Iterator(
        [
            "3310",
            "XD300S",
            "Hero 3",
            "Computer set",
            "Advance",
            "axs",
            "compaq",
            "Dell XPS",
            "Macbook",
            "Iphone 6",
            "Iphone 6S",
            "Desire",
        ]
    )
    type = ObjectModelType.back_office
    category = factory.SubFactory(CategoryFactory)
    manufacturer = factory.SubFactory(ManufacturerFactory)

    class Meta:
        model = AssetModel
        django_get_or_create = ["name"]


class DataCenterAssetModelFactory(DjangoModelFactory):
    name = factory.Iterator(["DL360", "DL380p", "DL380", "ML10", "ML10 v21"])
    type = ObjectModelType.data_center
    manufacturer = factory.SubFactory(ManufacturerFactory)
    height_of_device = factory.Iterator([1, 2, 3, 4])
    category = factory.SubFactory(DataCenterCategoryFactory)

    class Meta:
        model = AssetModel
        django_get_or_create = ["name"]


class EnvironmentFactory(DjangoModelFactory):
    name = factory.Iterator(["prod", "dev", "test"])

    class Meta:
        model = Environment
        django_get_or_create = ["name"]


class BusinessSegmentFactory(DjangoModelFactory):
    name = factory.Iterator(["IT", "Ads", "Research"])

    class Meta:
        model = BusinessSegment
        django_get_or_create = ["name"]


class ProfitCenterFactory(DjangoModelFactory):
    name = factory.Iterator(["PC1", "PC2", "PC3"])

    class Meta:
        model = ProfitCenter
        django_get_or_create = ["name"]


class ServiceFactory(DjangoModelFactory):
    name = factory.Iterator(["Backup systems", "load_balancing", "databases"])
    uid = factory.Sequence(lambda n: "sc-{}".format(n))
    business_segment = factory.SubFactory(BusinessSegmentFactory)
    profit_center = factory.SubFactory(ProfitCenterFactory)

    class Meta:
        model = Service
        django_get_or_create = ["name"]


class ServiceEnvironmentFactory(DjangoModelFactory):
    service = factory.SubFactory(ServiceFactory)
    environment = factory.SubFactory(EnvironmentFactory)

    class Meta:
        model = ServiceEnvironment
        django_get_or_create = ["service", "environment"]


class EthernetFactory(DjangoModelFactory):
    base_object = factory.SubFactory(BaseObjectFactory)
    label = factory.Sequence(lambda n: "ETH#{}".format(n))
    mac = factory.Sequence(next_mac)

    class Meta:
        model = Ethernet
        django_get_or_create = ["label"]


class EthernetWithIPAddressFactory(EthernetFactory):
    ipaddress = factory.RelatedFactory(
        "ralph.networks.tests.factories.IPAddressWithNetworkFactory", "ethernet"
    )


class ConfigurationModuleFactory(DjangoModelFactory):
    name = factory.Iterator(["ralph", "allegro", "auth", "order"])

    class Meta:
        model = ConfigurationModule
        django_get_or_create = ["name"]


class ConfigurationClassFactory(DjangoModelFactory):
    class_name = factory.Iterator(["www", "db", "worker", "cache"])
    module = factory.SubFactory(ConfigurationModuleFactory)

    class Meta:
        model = ConfigurationClass
        django_get_or_create = ["class_name"]


class MemoryFactory(DjangoModelFactory):
    base_object = factory.SubFactory(BaseObjectFactory)
    size = 8192
    speed = 1600
    model_name = "Samsung DDR3 DIMM"

    class Meta:
        model = Memory


class FibreChannelCardFactory(DjangoModelFactory):
    base_object = factory.SubFactory(BaseObjectFactory)
    firmware_version = factory.Iterator(["1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5"])
    model_name = "Saturn-X: LightPulse Fibre Channel Host Adapter"
    wwn = factory.Sequence(next_wwn)

    class Meta:
        model = FibreChannelCard


class ProcessorFactory(DjangoModelFactory):
    base_object = factory.SubFactory(BaseObjectFactory)
    speed = factory.Iterator([2500, 2600, 3000, 3200])
    cores = factory.Iterator([4, 8, 16])
    model_name = "Intel(R) Xeon(R) CPU"

    class Meta:
        model = Processor


class DiskFactory(DjangoModelFactory):
    base_object = factory.SubFactory(BaseObjectFactory)
    size = factory.Iterator([476, 256])
    serial_number = factory.Sequence(lambda n: "S1234{}".format(n))
    slot = factory.Iterator([0, 1, 2, 3, 4, 5, 6, 7])
    firmware_version = factory.Iterator(["1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5"])
    model_name = factory.Iterator(["ATA Samsung SSD", "Toshiba SSD"])

    class Meta:
        model = Disk
