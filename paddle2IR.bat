
call C:\Users\DELL\anaconda3\Scripts\activate.bat C:\Users\DELL\anaconda3\envs\paddle

cd C:\Program Files (x86)\Intel\openvino_2021.3.394\bin
call setupvars.bat

cd C:\Users\DELL\Desktop\Convert_Program
paddlex --export_inference --model_dir=./best_model --save_dir=./ --fixed_input_shape=[512,512]


paddle2onnx --model_dir ./inference_model --model_filename model.pdmodel --params_filename model.pdiparams --save_file ./inference_model/deeplab.onnx --opset_version 12

python "C:\Program Files (x86)\Intel\openvino_2021.3.394\deployment_tools\model_optimizer\mo_onnx.py" --input_model models.onnx --input_shape [1,3,512,512] --output_dir ./IR_model
pause