# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Minimalistic debian Vagrantfile for installation of basic dependencies.
# Missing postgresql installation.
#
# Authors: Marcin Mateusz Hanc.
# 2018

Vagrant.configure("2") do |config|
  config.vm.box = "bento/debian-8.10"

  config.vm.network "forwarded_port", guest: 80,   host: 8080, host_ip: "127.0.0.1"
  # config.vm.network "forwarded_port", guest: 8000, host: 8001, host_ip: "127.0.0.1"
  config.vm.network "private_network", ip: "10.0.42.42"

  config.vm.synced_folder ".", "/home/vagrant/zeus"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y build-essential
    apt-get install -y rsync
    apt-get install -y libicu-dev
    apt-get install -y libgmp-dev
    apt-get install -y libmpfr-dev
    apt-get install -y libmpc-dev
  SHELL
end
