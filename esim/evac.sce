config:
  destroy_time: 30
  engineName: sname 
  instance_time: 0 
  simName: evacuation 
sceType: EvacSim  
sceVersion: sce/v1 
scenario:          
  agents:             
  - aid: 0 
    coord:    
    - 0    
    - 0    
    rid: 0      
    strategy: OBJ_SMART   
    type: Normal                
  - aid: 1      
    coord:    
    - 0    
    - 0    
    rid: 0      
    strategy: OBJ_GREED   
    type: Normal                
  regions:     
  - entries:
    - coord:
      - 4   
      - 4   
      en_id: 0     
    exits:            
    - coord:          
      - 0          
      - 4          
      ex_id: 0            
    regionSize:           
    - 5                   
    - 5                   
    rid: 0 