from miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

#poller = MiFloraPoller("c4:7c:8d:61:a1:ac")
tomato_id = "c4:7c:8d:61:a1:ac"
#tomato_id = "cc4:7c:8d:61:a0:e4"

poller = MiFloraPoller(tomato_id)

print("Getting data from Mi Flora")
print("FW: {}".format(poller.firmware_version()))
print("Name: {}".format(poller.name()))
print("Temperature: {}".format(poller.parameter_value("temperature")))
print("Feuchtigkeit in Prozent: {}".format(poller.parameter_value(MI_MOISTURE)))
print("Light: {}".format(poller.parameter_value(MI_LIGHT)))
print("Naehrstatus: {}".format(poller.parameter_value(MI_CONDUCTIVITY)))
print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))
