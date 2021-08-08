#Docker will be used to create an isolated environment for AWS lambda and python packages
FROM lambci/lambda:build-python3.8

LABEL maintainer="contact@calculatestudentloans.com"

WORKDIR /var/task

# Fancy prompt to remind you are in zappashell
RUN echo 'export PS1="\[\e[36m\]zappashell>\[\e[m\] "' >> /root/.bashrc

#additional command here

CMD ["bash"]