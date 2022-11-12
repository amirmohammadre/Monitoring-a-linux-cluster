############################# Provision the VMs using Vagrant ############################# 

Vagrant.configure("2") do |config|
   
   #Worker_Node_1
   config.vm.define "node1" do |node1|
      node1.vm.box_download_insecure = true
      node1.vm.box = "generic/ubuntu2004"
      node1.vm.network "private_network", ip: "192.168.56.5"
      node1.vm.hostname = "node1"
      node1.vm.provider "virtualbox" do |v|
         v.name = "Node-1"
      end
   end

   #Worker_Node_2
   config.vm.define "node2" do |node2|
      node2.vm.box_download_insecure = true
      node2.vm.box = "generic/ubuntu2004"
      node2.vm.network "private_network", ip: "192.168.56.6"
      node2.vm.hostname = "node2"
      node2.vm.provider "virtualbox" do |v|
         v.name = "Node-2"
      end
   end

   #Worker_Node_3
   config.vm.define "node3" do |node3|
      node3.vm.box_download_insecure = true
      node3.vm.box = "generic/ubuntu2004"
      node3.vm.network "private_network", ip: "192.168.56.7"
      node3.vm.hostname = "node3"
      node3.vm.provider "virtualbox" do |v|
         v.name   = "Node-3"
      end
   end

end
