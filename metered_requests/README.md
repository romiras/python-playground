# metered_requests

A demonstration of a credit-based metering system for managing client requests. This system allows for rate-limiting requests by charging "credits" for each action and replenishing credits over time based on elapsed time since the last activity.

## Key Features

- **Credit-based Metering**: Charge a specific number of credits for each request.
- **Dynamic Replenishment**: Automatically replenish credits per second based on the time elapsed since the last client interaction.
- **Customizable Limits**: Configure initial credits, replenishment rates, and maximum caps for each client.

## Core Component: `CreditsRepository`

The `CreditsRepository` class handles all credit-related operations, including retrieving balances, calculating replenishment, and charging for actions.

### Configuration Parameters

The repository is initialized with a configuration dictionary:

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `initial_credits` | `int` | The starting credit balance for a new or unknown client. |
| `replenish_credits` | `int` | The number of credits added to the balance for every second of inactivity. |
| `charge_credits` | `int` | The number of credits to deduct for a single `charge()` call. |
| `max_credits` | `int` | The maximum balance a client can accumulate. |

## Quick Start

You can find a basic usage example in `main.py`. Here's a quick look:

```python
from credits_repository import CreditsRepository

config = {
    "initial_credits": 5,
    "replenish_credits": 1,
    "charge_credits": 1,
    "max_credits": 5
}

# Initialize the repository
db = None # Replace with a real DB connection as needed
credits_repo = CreditsRepository(db, config)

# Charge a client's account
client_id = 'example-client'
if credits_repo.charge(client_id):
    print("Action allowed")
else:
    print("Action denied: insufficient credits")
```

## Implementation Details

The system calculates the current balance lazily whenever `charge()` is called:
1. It retrieves the last known balance and the timestamp of the last update.
2. It calculates the elapsed time in whole seconds.
3. It multiplies elapsed seconds by `replenish_credits` and adds it to the old balance (clamped at `max_credits`).
4. If the new balance is sufficient, it deducts `charge_credits` and updates the permanent record.
