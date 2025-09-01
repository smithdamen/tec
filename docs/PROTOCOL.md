# Protocol v0 (JSON Lines)

Client→Server:
{"type":"LOGIN","name":"..."}
{"type":"MOVE","dx":1,"dy":0}
{"type":"WAIT"}

Server→Client:
{"type":"WELCOME","msg":"..."}
{"type":"POS","x":12,"y":34}
{"type":"VIEW","x":8,"y":10,"w":21,"h":11,"tiles":"..##..."}
{"type":"LOG","text":"..."}
{"type":"STATS","speed":1.0,"energy":0.5,"aps":1.0,"eta":0.5}
