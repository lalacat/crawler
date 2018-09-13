from test.framework.middleware import MiddlewareManager
from test.framework.objectimport.bulid_component_list import bulid_component_list


class ItemPipelineManager(MiddlewareManager):

    component_name = 'item pipeline'

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return bulid_component_list(settings['ITEM_PIPELINES'],cls.component_name)

    def _add_middleware(self, pipe):
        super(ItemPipelineManager, self)._add_middleware(pipe)
        if hasattr(pipe, 'process_item'):
            self.methods['process_item'].append(pipe.process_item)

    def process_item(self, item, spider):
        #  item的处理是串联式的处理
        return self._process_chain('process_item', item, spider)
