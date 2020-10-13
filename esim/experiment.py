import contexts
from adev.scenario_manager import *

scm = ScenarioManager('evac.sce')
rm = UniRegionManager()

# Regions
for region in scm.get_regions():
	rm.add_region_to_building(region['rid'], (region['regionSize'][0], region['regionSize'][1]))
	for entry in region['entries']:
		rm.add_entry_point_to_region(region['rid'], entry['en_id'], (entry['coord'][0],entry['coord'][1]))
	for exit in region['exits']:
		rm.add_exit_point_to_region(region['rid'], entry['ex_id'], (entry['coord'][0],entry['coord'][1]))

