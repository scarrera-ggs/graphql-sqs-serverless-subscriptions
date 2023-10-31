import json

import requests
from requests.adapters import HTTPAdapter


def create_inverter_mutation(
    inverter: dict,
    batteries: list,
    pvs: list,
) -> dict:
    query = """
    mutation ($input: CreateInverterInput!) {
        createInverter(input: $input) {
            inverter {
                name
                remoteId
                site {
                    name
                    remoteId
                    meters {
                        data {
                            name
                            remoteId
                        }
                    }
                }
                connectedBatteries {
                    remoteId
                }
                connectedPhotovoltaics {
                    remoteId
                }
            }
        }
    }
    """

    variables = {
        "input": {
            "remoteId": f"{inverter['remote_id']}",
            "name": f"{inverter['name'].upper()}",
            "operationalConstraints": {
                "efficiency": inverter["efficiency"],
                "ratedPower": inverter["rated_power"],
            },
            "adapterConfiguration": {
                "name": f"{inverter['adapter_name']}",
                "simulation": {"enabled": inverter["is_simulated"]},
            },
            "connectedBatteries": [
                {
                    "remoteId": f"{battery['remote_id']}",
                    "operationalConstraints": {
                        "ratedEnergy": battery["rated_energy"],
                        "ratedPower": battery["rated_power"],
                    },
                    "controlConstraints": {
                        "minimumStateOfCharge": battery["soh"],
                        "maximumStateOfCharge": battery["soc"],
                    },
                }
                for battery in batteries
            ],
            "connectedPhotovoltaics": [
                {
                    "remoteId": f"{pv['remote_id']}",
                    "operationalConstraints": {"ratedPower": pv["rated_power"]},
                }
                for pv in pvs
            ],
        }
    }

    return {"query": query, "variables": variables}


# queries = []
# for i in range(1_000):
#     print(i)
#     queries.append(
#         create_inverter_mutation(
#             inverter={
#                 "remote_id": f"test-inverter-{i+1}",
#                 "name": f"TEST INVERTER {i+1}",
#                 "efficiency": 90,
#                 "rated_power": 5000,
#                 "adapter_name": "Generac Pwrcell",
#                 "is_simulated": False,
#             },
#             batteries=[
#                 {
#                     "remote_id": f"test-battery-{i+1}",
#                     "rated_energy": 2500,
#                     "rated_power": 2500,
#                     "soh": 10,
#                     "soc": 90,
#                 }
#             ],
#             pvs=[
#                 {
#                     "remote_id": f"test-pv-{i+1}",
#                     "rated_power": 5000,
#                 }
#             ],
#         )
#     )

queries = [
    create_inverter_mutation(
        inverter={
            "remote_id": "test-inverter-1",
            "name": "TEST INVERTER 1",
            "efficiency": 90,
            "rated_power": 5000,
            "adapter_name": "Generac Pwrcell",
            "is_simulated": False,
        },
        batteries=[
            {
                "remote_id": "test-battery-1",
                "rated_energy": 2500,
                "rated_power": 2500,
                "soh": 10,
                "soc": 90,
            }
        ],
        pvs=[
            {
                "remote_id": "test-pv-1",
                "rated_power": 5000,
            }
        ],
    ),
    create_inverter_mutation(
        inverter={
            "remote_id": "test-inverter-2",
            "name": "TEST INVERTER 2",
            "efficiency": 90,
            "rated_power": 5000,
            "adapter_name": "Generac Pwrcell",
            "is_simulated": False,
        },
        batteries=[],
        pvs=[
            {
                "remote_id": "test-pv-2",
                "rated_power": 5000,
            }
        ],
    ),
    create_inverter_mutation(
        inverter={
            "remote_id": "test-inverter-3",
            "name": "TEST INVERTER 3",
            "efficiency": 90,
            "rated_power": 5000,
            "adapter_name": "Generac Pwrcell",
            "is_simulated": False,
        },
        batteries=[
            {
                "remote_id": "test-battery-3",
                "rated_energy": 2500,
                "rated_power": 2500,
                "soh": 10,
                "soc": 90,
            }
        ],
        pvs=[],
    ),
]

session = requests.Session()
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)

session.mount("https://", adapter)
session.mount("http://", adapter)

concerto_access_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJlbmJhbGFfdnBwIiwiZXhwIjoxNjg5NTIzMzM4LCJpYXQiOjE2ODk0MzY5MzgsImlzcyI6ImVuYmFsYV92cHAiLCJqdGkiOiI0Y2UwZDE3My1kZWQ4LTRkNDktOTE4ZC0zN2ZmZWY5NGE1ZGEiLCJuYmYiOjE2ODk0MzY5MzcsInNjb3BlcyI6WyJhcGlfZGlhZ25vc3RpY3NfcmVhZCIsImFzc2V0X21hbmFnZSIsImFzc2V0X3JlYWQiLCJjdXN0b21fcHJvcGVydHlfa2V5X2NyZWF0ZSIsImN1c3RvbV9wcm9wZXJ0eV9rZXlfZGVsZXRlIiwiZXZlbnRfbWFuYWdlIiwiZXZlbnRfbWV0cmljc191cGRhdGUiLCJldmVudF9yZWFkIiwiZm9yZWNhc3Rfd3JpdGUiLCJsZWdhY3lfdXNlcl9zY29wZSIsInByb2dyYW1fbWFuYWdlIiwicHJvZ3JhbV9yZWFkIiwiZXZlbnRfbWV0cmljc191cGRhdGUiLCJyZXBvcnRfcmVhZCIsInNpdGVfZGV2aWNlX3JlYWQiLCJzaXRlX3NpdGVfbWV0ZXJfbWFuYWdlIiwic2l0ZV9zaXRlX21ldGVyX3JlYWQiLCJ0ZWxlbWV0cnlfd3JpdGUiLCJ1c2VyX21hbmFnZSIsInVzZXJfcmVhZCIsInZwcF9tYW5hZ2UiLCJ2cHBfcmVhZCIsImRlZmF1bHRfYWN0aW9ucyJdLCJzdWIiOiI2MTk5ZGQ0NS1iMzdmLTRiOTgtODQxMS00MDBiOTZjZjczZGMiLCJ0eXAiOiJhY2Nlc3MiLCJ1c2VyIjp7ImlkIjoiNjE5OWRkNDUtYjM3Zi00Yjk4LTg0MTEtNDAwYjk2Y2Y3M2RjIn19.o0-16rru8NMhVJDLL9r1Z1wLzt0CUMrKgMeNuYo50GPG11yldF7RxZqUVZk107CgrcEtuSv534AMaHlNra4gFw"
response = session.post(
    url="http://localhost:3000/3.0/graphql",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {concerto_access_token}",
    },
    data=json.dumps(queries),
)

print(response)
print(response.json())
