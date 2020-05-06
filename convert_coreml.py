import coremltools
from keras.models import load_model

class_labels = ["Blue Tang","Cat Fish","Clown Fish","Rainbow Trout","Yellow Fin Tuna"]

model = load_model("model.h5")

coreml_model = coremltools.converters.keras.convert(model,
	input_names="image",
	image_input_names="image",
	class_labels=class_labels,
    input_name_shape_dict={'image': [None, 244, 244, 3]},
	is_bgr=True)

coreml_model.save("coreml_model.mlmodel")