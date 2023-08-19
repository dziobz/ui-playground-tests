from playwright.sync_api import Page, expect
import pytest

@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):

    return {
        **browser_type_launch_args,
        "headless": False,
    }

def test_dynamic_id(page: Page):
    page.goto("http://uitestingplayground.com/dynamicid")
    dynamicIDButton = page.get_by_role("button", name="Button with Dynamic ID")
    expect(dynamicIDButton).to_be_visible()
    dynamicIDButton.click()
    
