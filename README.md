# ProjectECE535
## Motivation
In modern cities, traffic issues have consistently been a vexing challenge. Urban traffic congestion, accidents, and traffic violations pose significant problems for city residents and traffic management authorities. To address these issues, we need an intelligent and efficient means to monitor and manage traffic violations. Concurrently, with the rapid development of the Internet of Things (IoT) and embedded technologies, we have the opportunity to apply these advanced technologies to traffic management to enhance urban traffic safety and efficiency. The license plate recognition system is a pivotal tool in modern traffic management as it automates the recognition of vehicle license plates, assisting law enforcement agencies in swiftly and accurately tracking vehicles involved in violations, thereby improving traffic safety and reducing traffic infractions.
## Design Goals:
1. Build license plate positioning module
2. Build number identification module
3. Testing the Accuracy of the Two Models
4. Continuously optimize models to improve accuracy
## Deliverables: 
1. Trained license plate location model and number recognition model
2. Use the test set to test the model to obtain the accuracy of the recognition results.
3. Report document
## System Blocks:
1. Convolutional neural network building module: responsible for positioning the license plate position
2. U-Net building block: used to identify license plate numbers.
3. Model testing module: Evaluate the recognition accuracy of license plate numbers after using two models.
## Hardware/Software Requirements:
1. Software: Python, TensorFlow, Keras
2. Hardware: Laptop with CUDA-enabled GPU
## Team member’s lead roles:
1. Xuan Zhang: License plate positioning module construction and training, report writing
2. Xujing Lei: Number identification module construction and training, report writing
3. Yunliang Zhong : Model testing and  optimization, report writing
## Project TimeLine:
1. Phase 1 (October): Processed all data,Model building
2. Phase 2 (November): model training and test
3. Phase 3 (December):Model optimization and report writing
## References:
1. U-Net paper.Link:[https://search.ebscohost.com/login.aspx?direct=true&AuthType=ip,sso&db=bth&jid=8WGI&site=eds-live&custid=umaah.](https://arxiv.org/pdf/1505.04597.pdf)
2. U-Net source code. Link:https://github.com/jakeret/tf_unet




