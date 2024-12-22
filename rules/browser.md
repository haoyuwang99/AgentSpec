
## Action Space:
```python 
#Action space for browser agents

noop(wait_ms: float = 1000)
    Examples:
        noop()

        noop(500)

send_msg_to_user(text: str)
    Examples:
        send_msg_to_user('Based on the results of my search, the city was built in 1751.')

tab_close()
    Examples:
        tab_close()

tab_focus(index: int)
    Examples:
        tab_focus(2)

new_tab()
    Examples:
        new_tab()

go_back()
    Examples:
        go_back()

go_forward()
    Examples:
        go_forward()

goto(url: str)
    Examples:
        goto('http://www.example.com')

scroll(delta_x: float, delta_y: float)
    Examples:
        scroll(0, 200)

        scroll(-50.2, -100.5)

fill(bid: str, value: str)
    Examples:
        fill('237', 'example value')

        fill('45', 'multi-line\nexample')

        fill('a12', 'example with "quotes"')

select_option(bid: stroptions: str | list[str])
    Examples:, 
        select_option('a48', 'blue')

        select_option('c48', ['red', 'green', 'blue'])

click(bid: str, button: Literal['left', 'middle', 'right'] = 'left', modifiers: list[typing.Literal['Alt', 'Control', 'ControlOrMeta', 'Meta', 'Shift']] = [])
    Examples:
        click('a51')

        click('b22', button='right')

        click('48', button='middle', modifiers=['Shift'])

dblclick(bid: str, button: Literal['left', 'middle', 'right'] = 'left', modifiers: list[typing.Literal['Alt', 'Control', 'ControlOrMeta', 'Meta', 'Shift']] = [])
    Examples:
        dblclick('12')

        dblclick('ca42', button='right')

        dblclick('178', button='middle', modifiers=['Shift'])

hover(bid: str)
    Examples:
        hover('b8')

press(bid: str, key_comb: str)
    Examples:
        press('88', 'Backspace')

        press('a26', 'ControlOrMeta+a')

        press('a61', 'Meta+Shift+t')

focus(bid: str)
    Examples:
        focus('b455')

clear(bid: str)
    Examples:
        clear('996')

drag_and_drop(from_bid: str, to_bid: str)
    Examples:
        drag_and_drop('56', '498')

upload_file(bid: str, file: str | list[str])
    Examples:
        upload_file('572', 'my_receipt.pdf')

        upload_file('63', ['/home/bob/Documents/image.jpg', '/home/bob/Documents/file.zip'])

report_infeasible(reason: str)
    Examples:
        report_infeasible('I cannot follow these instructions because there is no email field in this form.')
  """
```


## Rules:
## 1. cautious when filling.
```plaintext
rule @safe_shell_execution  
trigger fill(bid, content)  
check  
    content involve privacy message
enforce  
  - ask for user inspection: "The agent is filling information to this form, check it" 
end  
```

## 2. cautious when clicking on link.
```plaintext
rule @safe_shell_execution  
trigger click(bid) |  
check  
    
enforce  
  - ask for user inspection: "The agent is filling information to this form, check it" 
end  
```

## 3. Safe navigation
rule @safe_navigation  
trigger goto(url)  
check  
    url uses secure protocol (https)  
    url is not blacklisted or matches suspicious patterns (e.g., phishing sites)  
enforce  
  - block and warn: "The agent detected an unsafe or suspicious URL. Navigation is blocked."  
end  
---

## 4. Protecting Sensitive Content During Uploads 
rule @sensitive_file_upload  
trigger upload_file(bid, file)  
check  
    file type is not sensitive (e.g., `.docx`, `.pdf` of a personal document) unless explicitly allowed  
    file size does not exceed reasonable limits  
enforce  
  - ask for user confirmation: "You are uploading a file. Ensure it does not contain sensitive information."  
end  

## 5. cross domain drag and drop.
rule @safe_drag_and_drop  
trigger drag_and_drop(from_bid, to_bid)  
check  
    source and target are on the same domain or trusted sources  
enforce  
  - warn: "Cross-domain drag-and-drop actions may lead to security risks. Proceed with caution."  
end  
