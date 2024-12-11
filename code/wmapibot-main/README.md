# wmAPIbot


[wmApibot-catfacts-new.webm](https://media.github.webmethods.io/user/3509/files/4fa9e9f4-67d6-48a7-ae5a-17c5daf1e321)

## For Technical Documentation [Refer Here](resources/notes.md)

## Steps to Replicate

1. Clone the repository locally.
   ```
   git clone <repo link>
   cd wmapibot
   ```

2. In .env file add the HuggingFace Hub Token and Fireworks-ai API Key. Get HuggingFace Hub token from this [URL](https://huggingface.co/login). Get Fireworks-ai API Key from this [URL](https://app.fireworks.ai/login).
   ```
   HUGGINGFACEHUB_API_TOKEN = "<replace here>"
   FIREWORKS_API_KEY = "<replace here>"
   ```

3. Create a virtualenv and activate it using anaconda, if not present install it.

   ```
   conda create -n .venv python=3.11 -y
   conda activate .venv
   ```

4. Run the following command in the terminal to install necessary python packages:
   ```
   pip install -r requirements.txt
   ```

5. Run the following command in your terminal to start the chat UI:
   ```
   chainlit run app.py -w
   ```
   You will be redirected to the web browser.

6. Use the following command to deactivate the environment
   ```
   conda deactivate
   ```
---
