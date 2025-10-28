from fixtures import create_browser, create_simple_config
import pytest
import pytest_asyncio
import asyncio
from nodriver import Browser, Tab, Element, cdp


@pytest_asyncio.fixture
async def get_config(create_simple_config):
    return create_simple_config


@pytest_asyncio.fixture
async def get_browser(create_browser):
    return create_browser


@pytest.mark.asyncio
async def test_tab(get_browser: Browser) -> None:
    browser = get_browser
    tab = await browser.get('https://www.google.com/?hl=en')

    await tab
    assert 'google' in tab.url


@pytest.mark.asyncio
async def test_fetch_continue_request(get_browser: Browser) -> None:
    tab: Tab = await get_browser.get()

    async def handler(event: cdp.fetch.RequestPaused, tab: Tab) -> None:
        print('request paused event', event)
        await asyncio.sleep(1)
        print('continuing request')
        await tab.feed_cdp(cdp.fetch.continue_request(request_id=event.request_id))

    tab.add_handler(cdp.fetch.RequestPaused, handler)

    tab = await tab.get('https://google.com/?hl=en')

    assert tab is not None
