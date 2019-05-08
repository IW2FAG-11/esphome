from esphome.components import text_sensor
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import CONF_ID, CONF_LAMBDA, CONF_NAME, CONF_TEXT_SENSORS
from .. import custom_ns

CustomTextSensorConstructor = custom_ns.class_('CustomTextSensorConstructor')

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(CustomTextSensorConstructor),
    cv.Required(CONF_LAMBDA): cv.lambda_,
    cv.Required(CONF_TEXT_SENSORS):
        cv.ensure_list(text_sensor.TEXT_SENSOR_SCHEMA.extend({
            cv.GenerateID(): cv.declare_id(text_sensor.TextSensor),
        })),
})


def to_code(config):
    template_ = yield cg.process_lambda(
        config[CONF_LAMBDA], [], return_type=cg.std_vector.template(text_sensor.TextSensorPtr))

    rhs = CustomTextSensorConstructor(template_)
    var = cg.variable(config[CONF_ID], rhs)

    for i, conf in enumerate(config[CONF_TEXT_SENSORS]):
        text = cg.Pvariable(conf[CONF_ID], var.get_text_sensor(i))
        yield text_sensor.register_text_sensor(text, conf)