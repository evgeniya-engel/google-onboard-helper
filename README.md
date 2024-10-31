# google-onboard-helper
#### Setup instructions
1. Clone the reporitory on your machine:
```
git clone https://github.com/DB-Engineering/google-onboard-helper.git
```
2. Navigate to the cloned repository:
```
cd google-onboard-helper
```
3. Create a virtual environment (you only need to create it once, next time skip this step):
```
python3 -m venv .venv
```
4. Activate virtual environment:
* MacOs/Linux:
```
source .venv/bin/activate
```
* Windows:
```
.venv\Scripts\activate
```
5. Install requirements (you only need to create it once, next time skip this step.):
```
pip install -r requirements.txt
```
6. Run the app:
```
streamlit run helper_app.py
```
The app should open in a new browser window.
