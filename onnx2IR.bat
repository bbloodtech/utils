call C:\Users\DELL\anaconda3\Scripts\activate.bat C:\Users\DELL\anaconda3\envs\openvino
c:
cd C:\Program Files (x86)\Intel\openvino_2021.3.394\bin
call setupvars.bat

cd C:\Users\DELL\Desktop

python "C:\Program Files (x86)\Intel\openvino_2021.3.394\deployment_tools\model_optimizer\mo_onnx.py" --input_model deeplab.onnx --input_shape [1,3,512,512] --output_dir ./IR_model
