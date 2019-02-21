FROM gitpod/workspace-full

USER root
# add your tools here
RUN apt-get install -yq \
        texlive-latex-base \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        texlive-latex-extra \
        evince-common