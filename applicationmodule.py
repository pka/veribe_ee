# -*- coding: utf-8 -*-

from veriso.base.utils.utils import dynamic_import
from veriso.modules.applicationmodule_base import ApplicationModuleBase


class ApplicationModule(ApplicationModuleBase):
    """
    This is the minimum required implementation to have your own module
    """

    def __init__(self, veriso):
        super(ApplicationModule, self).__init__(veriso)

    def do_load_defects(self):
        # example of how to add your own defect layers or fields
        defects_module = 'veriso.modules.loaddefects_base'
        defects_module = dynamic_import(defects_module)
        d = defects_module.LoadDefectsBase(self.iface, self.module_name)

        fields = {
            'ogc_fid': {'widget': 'TextEdit',
                        'readonly': True,
                        'config': {"Editable": False}},
            'topic': {'widget': 'Enumeration',
                      'default': 'Bodenbedeckung',
                      'alias': 'Topic:',
                      'writable_only_by': ['agi', 'avor']},
            'bezeichnun': {
                'widget': 'Enumeration',
                'alias': 'Bezeichnung:',
                'writable_only_by': ['agi', 'avor']},
            'abrechnung': {
                'widget': 'Enumeration',
                'default': 'PNF',
                'alias': 'Abrechnung:',
                'writable_only_by': ['agi', 'avor']},
            'bem_avor': {
                'widget': 'TextEdit',
                'alias': 'Bemerkung AVOR:',
                'config': {"IsMultiline": True},
                'writable_only_by': ['agi', 'avor']},
            'datum': {'widget': 'Hidden'},
            'bem_nfg': {
                'widget': 'TextEdit',
                'alias': 'Bemerkung NFG:',
                'config': {"IsMultiline": True},
                'writable_only_by': ['agi', 'geometer']},
            'forstorgan': {
                'widget': 'Enumeration',
                'alias': 'Forstorgan:',
                'writable_only_by': ['agi', 'forst']},
            'bem_forst': {
                'widget': 'TextEdit',
                'alias': 'Bemerkung Forst:',
                'config': {"IsMultiline": True},
                'writable_only_by': ['agi', 'forst']},
            'verifikati': {
                'widget': 'Enumeration',
                'alias': 'Verifikation:',
                'writable_only_by': ['agi']},
            'bem_verifi': {
                'widget': 'TextEdit',
                'alias': 'Bemerkung Verifikation:',
                'config': {"IsMultiline": True},
                'writable_only_by': ['agi']},
            'erledigt': {
                'widget': 'CheckBox',
                'alias': 'Erledigt:',
                'config': {
                    'CheckedState': 't',
                    'UncheckedState': 'f'},
                'writable_only_by': ['agi']}}

        d.layers['point']['fields'] = fields
        d.layers['line']['fields'] = fields
        d.layers['polygon']['fields'] = fields

        d.layers['point']['readonly'] = True
        d.layers['line']['readonly'] = True
        d.layers['polygon']['readonly'] = True

        return d.run()
