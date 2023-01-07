::转换格式：PascalVOC、MSCOCO、SEG
call C:\Users\DELL\anaconda3\Scripts\activate.bat C:\Users\DELL\anaconda3\envs\paddle
paddlex --data_conversion --source labelme --to SEG^
		--pics .\JPEGImages ^
        --annotations .\Annotations ^
        --save_dir .\dataset_seg
		
pause