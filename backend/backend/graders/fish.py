from flask import abort, current_app
from backend.model import Fish, Bin, db

from datetime import datetime, timedelta, UTC
import trio

import signal
from typing import Any

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


from itertools import count

async def connect_to_grader(host, port):
    """Attempt to connect to the fish grader and return the connected socket."""
    for number in count():
        print(f'Reconnect {number}')
        try:
            logger.info(f"Attempting connect to {host}")
            s = await trio.open_tcp_stream(host, port)
            logger.info(f"Connected to {host}")
            return s
        except Exception as e:
            logger.error(f"Connection error for {host}: {e}. Retrying in 5 seconds...")
            await trio.sleep(5)


async def fish_grader_task(host) -> None:
    """Main task to handle connection and communication with the fish grader."""
    port = 5010
    while True:
        s = await connect_to_grader(host, port)
        await communicate(s, host)


async def communicate(s, host):
    """Handle the communication loop with the fish grader."""
    cmd = str(64).encode("ascii").hex()
    msg = f"0221363609313709{cmd}093138093103"
    msg = bytes.fromhex(msg)

    fields = {
        "1": "Weight", "2": "Unit", "3": "Sweight", "7": "WeightQuality",
        "8": "WeighingCount", "4": "Output", "10": "BatchId", "11": "Status",
        "14": "MaterialNumber", "19": "Key"
    }

    try:
        while True:
            await s.send_all(msg)
            data = await s.receive_some(256)
            data = data.decode("ascii").split("\t")[1:-4]

            if len(data) >= 22:
                res = {fields.get(data[i], data[i]): data[i + 1] for i in range(0, len(data), 2)}
                res["ip"] = host.split(".")[-1]
                fish_add(res)

    except trio.Cancelled:
        logger.info(f"Gracefully cleaning up connection with {host}...")
        await s.aclose()
        raise
    except (trio.BrokenResourceError, trio.ClosedResourceError, trio.TooSlowError) as e:
        logger.error(f"Communication error with {host}: {e}. Reconnecting...")
    except Exception as e:
        logger.error(f"Unexpected error during communication with {host}: {e}")



async def start_fish_grader_tasks() -> None:
    """Function to start the background tasks for fish graders."""

    def terminate(*_: Any) -> None:
        nursery.cancel_scope.cancel()

    signal.signal(signal.SIGTERM, terminate)

    logger.info(f"Current app in start tasks function: {current_app.name}")

    async with trio.open_nursery() as nursery:
        logger.info("Starting fish grader tasks...")

        for ip in current_app.config.get(f'GRADER_IPS').split(","):
            logger.info(f"Connecting to {ip}")
            nursery.start_soon(fish_grader_task, ip.strip())


def fish_add(data) -> None:
    dg = '[12.38] DualGrader Bin'
    ## Mapping dictionary used in FishResource
    bins = {"151": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "12", "8": "13", "9": "14",
                    "10": "15"},
            "152": {"1": "2", "2": "3", "3": "4", "4": "5", "5": "6", "6": "7", "7": "8", "8": "14", "9": "15"}}

    ## Mapping dictionary used in FishResource
    bins = {"6": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "12", "8": "13", "9": "14",
                    "10": "15"},
            "17": {"1": "2", "2": "3", "3": "4", "4": "5", "5": "6", "6": "7", "7": "8", "8": "14", "9": "15"}}

    time_threshold = datetime.now(UTC) - timedelta(hours=48)
    db.session.query(Fish).filter(Fish.datetime < time_threshold).delete(synchronize_session=False)

    # Validate the required fields
    required_fields = ['ip', 'Output', 'Sweight', 'MaterialNumber']
    for field in required_fields:
        if field not in data:
            abort(400, f'expected_{field}')

    new_fish = Fish(
        ip=data['ip'],
        bin=data['Output'],
        weight=data['Sweight'],
        product=data['MaterialNumber']
    )

    db.session.add(new_fish)

    grader = bins.get(data["ip"])
    if grader:
        bin_id = grader.get(data["Output"])
        if bin_id:
            existing_bin = Bin.query.filter_by(bin_name=f"{dg} {bin_id}").first()
            if existing_bin:
                existing_bin.weight += float(data['Sweight'])
                existing_bin.fish_weight = float(data['Sweight'])
                existing_bin.bin = data["Output"]
                existing_bin.grader = data["ip"]
                existing_bin.count += 1
            else:
                new_bin = Bin(bin_name=f"{dg} {bin_id}", weight=float(data['Sweight']), count=1)
                db.session.add(new_bin)

    db.session.commit()

    return {"id":new_fish.id}, 201
