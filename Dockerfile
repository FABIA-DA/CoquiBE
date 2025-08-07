FROM continuumio/miniconda3@sha256:4a2425c3ca891633e5a27280120f3fb6d5960a0f509b7594632cdd5bb8cbaea8

WORKDIR /app

# Create environment
COPY . .
RUN conda env create -f environment.yml

# Set the environment as the default
RUN echo "conda activate coqui-be-env" > ~/.bashrc
ENV PATH=/opt/conda/envs/coqui-be-env/bin:$PATH

RUN apt-get install espeak-ng

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]