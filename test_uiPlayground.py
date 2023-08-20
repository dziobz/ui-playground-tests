from playwright.sync_api import Page, expect, TimeoutError
import pytest

def on_dialog(dialog):
    print("Dialog opened:", dialog)
    dialog.accept()

def on_prompt(prompt):
    print("Prompt opened: ", prompt)
    prompt.accept()

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

    
def test_class_attr(page: Page):
    page.on("prompt", on_prompt)
    page.goto("http://uitestingplayground.com/classattr")
    blue_btn = page.locator("button.btn-primary")
    expect(blue_btn).to_be_visible()
    blue_btn.click()


def test_hidden_layers(page: Page):
    page.goto("http://uitestingplayground.com/hiddenlayers")
    btn = page.locator("#greenButton")
    btn.click()
    with pytest.raises(TimeoutError):
        btn.click(timeout=2000)


def test_load_delay(page: Page):
    page.goto("http://uitestingplayground.com/loaddelay")
    button = page.get_by_role("button", name="Button Appearing After Delay")
    page.wait_for_load_state()
    expect(button).to_be_visible()
    button.click()


def test_ajax_data(page: Page):
    page.goto("http://uitestingplayground.com/ajax")
    button = page.get_by_role("button", name="Button Triggering AJAX Request")
    data = page.locator("p.bg-success")
    button.click()
    data.wait_for()
    expect(data).to_have_text("Data loaded with AJAX get request.")


def test_client_side_delay(page: Page):
    page.goto("http://uitestingplayground.com/clientdelay")
    button = page.get_by_role("button", name="Button Triggering Client Side Logic")
    button.click()
    data = page.locator("p.bg-success")
    data.wait_for()
    expect(data).to_have_text("Data calculated on the client side.")
