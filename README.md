# [UCSD Machine Learning Engineering & AI Bootcamp](https://career-bootcamp.extension.ucsd.edu/programs/machine-learning-engineering/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mentalhealthintech.streamlit.app/)
## Mental Health in the Tech Industry Q&A Chatbot (Capstone Project)


The tech industry thrives on innovation and passionate individuals.

However, demanding work environments can contribute to stress, anxiety, and burnout among employees. While data suggests this is a significant issue, current analysis methods lack accessibility and user-friendliness.

To create a more supportive and productive tech landscape, fostering open communication about mental health is essential.  By destigmatizing the topic, we can encourage employees to seek help and build a culture of well-being.

This initiative proposes a web-based tool that transforms mental health data into clear and engaging insights. This empowers both tech professionals and the public to understand the scope of the issue and its impact on the workforce.

With increased awareness and accessible data through the use of a Retrieval-Augmented Generation (RAG) chatbot in this case, we can identify trends, develop targeted solutions, and ultimately build awarenes towards healthier workplaces in the tech industry for all.


## Quickstart

### Setup Python environment

The Python version used when this was developed was 3.10.14


```bash
python -mvenv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

If you run into issues related to hnswlib or chroma-hnswlib while installing requirements you may need to install system package for the underlying package.

For example, on Ubuntu 22.04 this was needed before pip install of hnswlib would succeed.

```bash
sudo apt install python3-hnswlib
```

### Setup .env file with API tokens needed.

```
HUGGINGFACEHUB_API_TOKEN="<Put your token here>"
```

### Setup Streamlit app secrets.

#### 1. Set up the .streamlit directory and secrets file.

```bash
mkdir .streamlit
touch .streamlit/secrets.toml
chmod 0600 .streamlit/secrets.toml
```

#### 2. Edit secrets.toml

**Either edit `secrets.toml` in you favorite editor.**

```toml
HUGGINGFACEHUB_API_TOKEN="<Put your token here>"
```

**Or, you can just reuse .env contents from above.**

```bash
cat < .env >> .streamlit/secrets.toml
```

### Verify Environment

1. Check that LangChain dependencies are working.

```bash
python basic_chain.py
```

2. Check that Streamlit and dependencies are working.

```bash
streamlit run streamlit_app.py
```

## Example Queries

- According to the 'Mental Health in the Tech Industry Survey', what are the most common mental health challenges faced by tech industry professionals?

- The 'Mental Health in the Tech Industry Survey' reports on the prevalence of burnout, anxiety, and depression among tech industry workers. What are the key findings in this regard?

- The 'Mental Health in the Tech Industry Survey' recommends strategies and resources to support the mental well-being of tech industry professionals. What are some of these recommendations?

- How does the 'Mental Health in the Tech Industry Survey' compare the mental health experiences of tech industry workers to those in other industries?

- The 'Mental Health in the Tech Industry Survey' explores the impact of workplace culture, job demands, and work-life balance on the mental health of tech industry professionals. What insights does it provide in this regard?

- The 'Mental Health in the Tech Industry Survey' makes recommendations for tech companies to promote mental health and prevent burnout among their employees. What are some of these recommendations?

- How does the 'Mental Health in the Tech Industry Survey' suggest that tech industry professionals can prioritize their own mental health and well-being in the workplace?

- What are some of the key takeaways from the 'Mental Health in the Tech Industry Survey' that can inform mental health policies and practices in the tech industry?

- The 'Mental Health in the Tech Industry Survey' highlights the need for greater awareness, support, and resources for mental health in the tech industry. What actions does it recommend for tech industry leaders, managers, and HR professionals to address mental health challenges in the workplace?

- What are some of the key findings from the 'Mental Health in the Tech Industry Survey' that can inform mental health policies and practices in the tech industry, and what actions does it recommend for tech industry leaders, managers, and HR professionals to address mental health challenges in the workplace?


## Underlying Data Used

Original 2016-2023 seed data from the [OSMI Mental Health in Tech Survey](https://osmhhelp.org/research.html)

A [Google Forms Survey](https://forms.gle/CzRFVaxMy5S3asVp6)

A [Google Sheets spreadsheet](https://docs.google.com/spreadsheets/d/1Oj8ROLPcsq_I8h3Au7bE9cUSFhTFQx3eEIr8BXV1Jx4/edit?usp=sharing) collecting the newest answers to the survey, on top of the historical data.

The [source CSV file](https://docs.google.com/spreadsheets/d/1Oj8ROLPcsq_I8h3Au7bE9cUSFhTFQx3eEIr8BXV1Jx4/export?format=csv) that is produced and downloaded into the application for use in the RAG chain.

The model used in the RAG chain is HuggingFace's [Zephyr 7B beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)


## Licensing

While the code contained in this repo is covered by an Apache-2.0 License, the underlying data (including the survey applied and it's results) is available through a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)
