# GPT-2 Discord Chat Bot (2021)

<img src="The_Child_Small.webp" alt="Icon" style="display: block; margin: auto;" />

## Overview
This is a Discord bot built with a custom-trained GPT-2 model for chat interaction. The bot uses CSV files as training data to power its conversational AI.

## Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup
1. Create `scripts` directory for CSV training data
2. Ensure proper Discord bot token in environment in `.env`
3. Configure channel IDs in the code

## Features
- Channel-specific message tracking
- Quit command: @BotUser !quit in designated channel
- Model training workflow for conversation datasets

## Usage
1. Run the bot with:
```bash
python bot.py
```
2. Interact in designated channels to see responses

## Notes
The bot uses CSV files in the `scripts` directory as training data for its GPT-2 model. Model training details are in `model/model_train_upload_workflow.py`.