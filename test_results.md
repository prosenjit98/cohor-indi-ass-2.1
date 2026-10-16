# IT Helpdesk Classification - Test Results

## Summary Statistics

- **Total Tests**: 25
- **Category Accuracy**: 68.0%
- **Priority Accuracy**: 80.0%
- **Overall Accuracy**: 52.0%

## Performance by Test Category

- **clear_case**: 60.0% (9/15)
- **ambiguous**: 0.0% (0/5)
- **multi_issue**: 50.0% (1/2)
- **edge_case**: 100.0% (3/3)

## Detailed Test Results

| ID | Category | Input | Expected | Actual | Match |
|-----|----------|-------|----------|--------|-------|
| 1 | clear_case | My laptop is not connecting to the office Wi-Fi.... | Network & Connectivity / Medium | Network & Connectivity / High | ⚠️ |
| 2 | clear_case | I forgot my password and need to reset it.... | Account & Access / Medium | Account & Access / Medium | ✅ |
| 3 | clear_case | Microsoft Word keeps crashing when I try to open d... | Software & Applications / High | Software & Applications / High | ✅ |
| 4 | clear_case | The printer on the 3rd floor is showing as offline... | Hardware Issues / Medium | Hardware Issues / Medium | ✅ |
| 5 | clear_case | I received a suspicious email asking me to verify ... | Security / High | Security / High | ✅ |
| 6 | clear_case | Can't access my email. It says authentication fail... | Email & Communication / High | Email & Communication / High | ✅ |
| 7 | clear_case | VPN connection keeps dropping every few minutes.... | Network & Connectivity / High | Network & Connectivity / Medium | ⚠️ |
| 8 | clear_case | My computer won't turn on at all. The power light ... | Hardware Issues / High | Hardware Issues / Critical | ⚠️ |
| 9 | clear_case | Need access to the Finance shared folder for the q... | Account & Access / Medium | Email & Communication / Medium | ⚠️ |
| 10 | clear_case | Zoom meeting won't start. Getting error code 5003.... | Email & Communication / High | Software & Applications / High | ⚠️ |
| 11 | clear_case | My mouse is not working. I've tried different USB ... | Hardware Issues / Medium | Hardware Issues / Medium | ✅ |
| 12 | clear_case | Need to install Adobe Acrobat Pro on my new laptop... | Software & Applications / Medium | Software & Applications / Medium | ✅ |
| 13 | clear_case | My account is locked after entering the wrong pass... | Account & Access / High | Account & Access / High | ✅ |
| 14 | clear_case | Internet is extremely slow today. Takes forever to... | Network & Connectivity / Medium | Network & Connectivity / Medium | ✅ |
| 15 | clear_case | My antivirus is showing a virus detection alert.... | Security / Critical | Security / High | ⚠️ |
| 16 | ambiguous | Something is wrong with my computer.... | Hardware Issues or Software & Applications / Medium | Hardware Issues / Medium | ⚠️ |
| 17 | ambiguous | URGENT!!! Need help ASAP!!!... | Unknown / Medium | Hardware Issues / High | ⚠️ |
| 18 | ambiguous | Everything is slow.... | Software & Applications or Network & Connectivity / Medium | Software & Applications / Medium | ⚠️ |
| 19 | ambiguous | The thing isn't working.... | Unknown / Medium | Hardware Issues / Medium | ⚠️ |
| 20 | ambiguous | Can you help me?... | Unknown / Low | Low / Low | ⚠️ |
| 21 | multi_issue | Can't login to my computer and the printer is also... | Account & Access / High | Account & Access / High | ✅ |
| 22 | multi_issue | My computer is running slow, I can't access email,... | Email & Communication / High | Software & Applications / High | ⚠️ |
| 23 | edge_case | My computer is making weird noises and smells like... | Hardware Issues / Critical | Hardware Issues / Critical | ✅ |
| 24 | edge_case | Everyone in the office lost internet connection at... | Network & Connectivity / Critical | Network & Connectivity / Critical | ✅ |
| 25 | edge_case | How do I change the background on my desktop?... | Software & Applications / Low | Software & Applications / Low | ✅ |
