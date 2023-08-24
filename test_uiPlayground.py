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


def test_click(page: Page):
    page.goto("http://uitestingplayground.com/click")
    button = page.get_by_role("button", name="Button That Ignores DOM Click Event")
    button.click()
    expect(button).to_have_class("btn btn-success")
    print("\nButton is not clickable/is not reacting anymore")


def test_text_input(page: Page):
    page.goto("http://uitestingplayground.com/textinput")
    button = page.locator("#updatingButton")
    input = page.get_by_label("Set New Button Name")
    input.fill("Python")
    button.click()
    expect(button).to_have_text("Python")


def test_scrollbars(page: Page):
    page.goto("http://uitestingplayground.com/scrollbars")
    button = page.locator("#hidingButton")
    button.scroll_into_view_if_needed()
    button.click()
    # only .click works as well, it scrolls automatically to the element


def test_dynamic_table(page: Page):
    page.goto("http://uitestingplayground.com/dynamictable")
    label = page.locator("p.bg-warning").inner_text()
    label_percentage = label.split()[-1] # Get percentage number from the label
    
    ### First method
    """ 
    percentage = label.split()[-1]
    column_headers = page.get_by_role("columnheader")
    cpu_column = None

    for index in range(column_headers.count()):
        column_header = column_headers.nth(index)

        if column_header.inner_text() == "CPU":
            cpu_column = index
            break
    assert cpu_column != None

    rowgroup = page.get_by_role("rowgroup").last
    chrome_row = rowgroup.get_by_role("row").filter(has_text='Chrome')

    chrome_cpu =chrome_row.get_by_role("cell").nth(cpu_column)
    expect(chrome_cpu).to_have_text(percentage) """

    ### Second mehthod
    rowgroup = page.get_by_role("rowgroup")
    chrome_row = rowgroup.get_by_role("row", name="Chrome").inner_text().split()
    
    table_percentage = [e for e in chrome_row if "%" in e][0]
    print(label_percentage, table_percentage)
    assert table_percentage == label_percentage


def test_verify_text(page: Page):
    page.goto('http://uitestingplayground.com/verifytext')
    text = page.locator("div.bg-primary").get_by_text("Welcome", exact=False)
    expect(text).to_have_text("Welcome UserName!") 
    text.dblclick()


def test_progress_bar(page: Page):
    page.goto("http://uitestingplayground.com/progressbar")
    start_btn = page.get_by_role("button", name="Start")
    stop_btn = page.get_by_role("button", name="Stop")
    progress = page.get_by_role("progressbar")
    start_btn.click()

    while True:
        valuenow = int(progress.get_attribute("aria-valuenow"))
        
        if valuenow >=75:
            break

    stop_btn.click()
    assert valuenow >= 75
    

def test_visibility(page: Page):
    page.goto("http://uitestingplayground.com/visibility")
    hide_btn = page.get_by_role("button", name="Hide")
    removed_btn = page.get_by_role("button", name="Removed")
    zero_width_btn = page.get_by_role("button", name="Zero Width")
    overlapped_btn = page.get_by_role("button", name="Overlapped")
    opacity0_btn = page.get_by_role("button", name="Opacity 0")
    visibility_hidden_btn = page.get_by_role("button", name="Visibility Hidden")
    display_none_btn = page.get_by_role("button", name="Display None")
    offscreen_btn = page.get_by_role("button", name="Offscreen")

    hide_btn.click()
    expect(removed_btn).not_to_be_visible()
    expect(zero_width_btn).to_have_css("width", "0px")
    with pytest.raises(TimeoutError):
        overlapped_btn.click(timeout=1500)
    expect(opacity0_btn).to_have_css("opacity", "0")
    expect(visibility_hidden_btn).to_be_hidden()
    expect(display_none_btn).to_be_hidden()
    expect(offscreen_btn).not_to_be_in_viewport()


def test_sample_app(page: Page):
    page.goto("http://uitestingplayground.com/sampleapp")
    label = page.locator("#loginstatus")
    username = "TestLogin"
    password = "pwd"
    username_input = page.get_by_placeholder("User Name")
    password_input = page.get_by_placeholder("********")
    button = page.locator("#login.btn.btn-primary")

    username_input.fill(username)
    password_input.fill(password)
    button.click()
    expect(label).to_have_text(f"Welcome, {username}!")


def test_mouseover(page: Page):
    page.goto("http://uitestingplayground.com/mouseover")
    clickme = page.get_by_text("Click me")
    clickcount = page.locator("#clickCount")
    clickme.hover()
    activelink = page.get_by_title("Active Link")
    activelink.click(click_count=2)
    expect(clickcount).to_have_text("2")


def test_nbsp(page: Page):
    page.goto("http://uitestingplayground.com/nbsp")
    button = page.locator("//button[text()='My\u00a0Button']")
    button.click()


def test_overlapped_element(page: Page):
    page.goto("http://uitestingplayground.com/overlapped")
    input = page.get_by_placeholder("Name")

    div = input.locator("..") # <-- Selects div parent element 
    div.hover()

    page.mouse.wheel(0, 200) # Scroll horizontally 200px
    
    page.wait_for_timeout(100)
    data = "python"
    input.fill(data)
    expect(input).to_have_value(data)

    

