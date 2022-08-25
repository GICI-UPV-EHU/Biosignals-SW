# Biosignals-SW

<p align="center">
<img src="https://user-images.githubusercontent.com/46607004/154055355-a45a597b-4c16-4460-a285-ad0554636bdf.png" alt="drawing" width="200"/>
</p>

Este repositorio se destinará a los desarrollos SW con placas low-cost: Medida y comunicación.

Estos desarrollos van encaminados al manejo y la gestión de datos que, una vez llegan a los diferentes dispositivos Low-cost, se preparan ordenadamente para ser enviados vía wifi, cumplindo con las necesidades de comunicación (protocolos, frecuencias de muestreo, etc.). 

Inicialmente estará destinado al trabajo que desarrollará Imanol Ayude en su TFM, en el marco del Máster en Ingeniería de Control, Automatización y Robótica.

Actualmente este repositorio contiene el código fuente del TFM desarrollado por Oinatz Aspiazu para el Máster de Ingeniería Biomédica. En el mismo, se pretende continuar el trabajo de Imanol Ayude para diseñar una solución cliente-servidor que sepa recoger los valores de los sensores y guardarlos en una base remota a través del multiproceso.

También se implanta una pequeña página web que lee los datos de la Base de Datos del diseño.

Carpetas:

- sensores_raspberry: Contiene todo el código de la implantación realizada en Raspberry Pi
- sens_local: Contiene la página Web realizada
- esp32_sensors: Contiene diversas pruebas realizadas con el dispositivo ESP32 (descartado para el proyecto como se detalla en la memoria)
- memoria: Contiene la memoria del proyecto
- presentación: Contiene la presentación de la defensa del TFM
