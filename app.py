from flask import Flask, request, redirect
from random import randint
import logging

from opentelemetry import trace, metrics
from opentelemetry.trace import Status, StatusCode

# Get tracer and meter
tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")

# Create counter metric
roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value",
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return redirect("/rolldice")

@app.route("/rolldice")
def roll_dice():
    with tracer.start_as_current_span("roll") as roll_span:
        player = request.args.get('player', default="anonymous", type=str)
        try:
            result = roll()
            roll_span.set_attribute("roll.value", result)
            roll_counter.add(1, {"roll.value": str(result)})

            logger.warning("%s is rolling the dice: %s", player, result)
            return str(result)

        except Exception as e:
            roll_span.record_exception(e)
            roll_span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.error("Exception while rolling: %s", e)
            return f"Error: {str(e)}", 500

def roll():
    value = randint(1, 6)
    if value == 6:
        raise ValueError("Unlucky roll: 6 triggered an exception!")
    return value
