# Belgrade Flat Watcher

Telegram bot for monitoring apartment listings in Belgrade.

The bot searches apartments using Selenium, allows users to subscribe to search filters, stores previously seen listings in SQLite, and sends notifications only about new apartments.

## Features

* Search apartments by:

    * rooms count
    * price range
    * square range
* Telegram subscriptions
* Daily notifications about new apartments
* Selenium-based web scraping
* Repository-Service architecture
* Unit and integration tests
* Allure reports
* GitHub Actions CI

## Architecture

```text
                         main.py
                            │
                            ▼
                 TelegramApplication
                            │
                            ▼
                  TelegramController
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   DialogHandler   SubscriptionHandler   FlatsService
                                              │
                 ┌────────────────────────────┼────────────────────────────┐
                 │                            │                            │
                 ▼                            ▼                            ▼
   SubscriptionRepository          SeenFlatRepository              SearchExecutor
                 │                            │                            │
                 └──────────────┬─────────────┘                            ▼
                                ▼                                    SearchService
                         SQLite Database                                  │
                                                                          ▼
                                                                  Selenium WebDriver
                                                                          │
                                                                          ▼
                                                                 Real Estate Websitee
```

## Tech Stack

* Python
* python-telegram-bot
* Selenium
* SQLAlchemy
* SQLite
* pytest
* pytest-asyncio
* pytest-mock
* Allure Report
* GitHub Actions
* uv

## Testing

The project includes:

* Repository tests
* Service tests
* Integration tests for Selenium search
* Automated CI with GitHub Actions
* Allure test reports

## Continuous Integration

Every push to the repository automatically:

* installs dependencies
* runs tests
* generates Allure results
* publishes the test report via GitHub Pages

## Test Report

The latest Allure report is available here:

**<add GitHub Pages URL here>**

## Run locally

```bash
uv sync
python main.py
```

## Run tests

```bash
uv run pytest tests
```
