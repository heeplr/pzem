

read from PZEM-0xx Energy Meter Modules and output as json

```sh
$ pzem | head -n1 | jq
```

```json
{
  "voltage": 13.02,
  "current": 3.2200000000000006,
  "power": 41.6,
  "energy": 2.7774,
  "voltage_alarm": {
    "low": false,
    "high": false
  },
  "current_range": "50A"
}
```
