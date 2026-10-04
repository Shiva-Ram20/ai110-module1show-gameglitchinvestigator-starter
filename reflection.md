# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
-> A game where you inputted numbers and it checked it was lower, higher or the number itself
-> You had X amount of guesses depending on the difficulty
-> There were a couple of noticeable problems like the hint messages
-> Other bugs were more noticeable when I was adjusting the code

- List at least two concrete bugs you noticed at the start  
-> Number doesn’t change regardless of the mode
-> Hint messages were inaccurate

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Mormal Difficulty: 39, 62, 84, 93, 99, 100 | Hint message suppose to be higher for 1 & lower for the rest | hint message said higher for them all | None (Logical Error) |
| Easy Difficulty: 15, 5, 1 | attempts to reflect the amount of attempts I actual have | It showed 1 less on the first load | None (Logical Error) |
| Hard Mode: 56, Swap to Easy Mode and 56 was the secret still | Change the number to match the appropriate range | Kept the same number which lead to the secret being out of bounds | None (Logical Error) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
-> Claude & Gemini
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
-> The AI had suggested at the start that the hint messages were swapped. It was correct and also something that I noticed. I verified the suggestion through testing within the program across the various difficulties. I implemented their suggestion of swapping the hint messages and moved the block of code from app.py to logic_utils.py.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
When fixing the code's bugs, the AI had suggested to adjust the input to deny decimal values instead of rounding them. I denied it cause I did not really see a huge benefit from deny decimal values. I thought that it would just be complicating the system and over-engineered the code. I verified my version by running pytest and testing decimal inputs in the UI to ensure it handled them correctly.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
-> I would refresh the game within my localhost and test to see if the bug was corrected.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
-> One test was for the hint messages. Using the developer debug info, I was able to guess above and below the secret to see if the hint messages were accurate.
- Did AI help you design or understand any tests? How?
The AI helped me to understand the tests. At first, I was unsure about if the modes were actually presenting the correct numbers for its range. But, as I divided deeper into the code with Claude, I was able to figure and identity the issues.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
-> If I had to explain it to a friend, I'd say that Streamlit reruns the entire Python script from top to bottom. Because of that, regular variables would normally reset to zero. Session state acts like a persistent memory bank that saves important data so it doesn't get lost when the page refreshes.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
-> Whether it is for simple problems like two values being swapped or intricate problems such as fixing a code block so that difficulties properly function, using AI to debug your programs are super useful.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
-> I would like to work on wording my AI prompts better. There were 1 or 2 cases where due to the wording, I had to follow up and ask another question with a separate AI prompt. If I had condensed and linked both of the prompts, I could have gotten a more coherent and in-depth response.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
-> This project has changed the way I think about AI generated code as it showed me how little and big the errors can be within the code. AI generated code isn't to be blindly trusted. It should be reviewed for errors and bugs before being published.
