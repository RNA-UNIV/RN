import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import Callback
from IPython import display
import io
import base64
import random

class ImageVisualizer(Callback):
   """
    Callback para visualizar im�genes durante el entrenamiento de un modelo.

    Parameters:
        model (Model): El modelo de Keras que se est� entrenando.
        in_images (ndarray): Las im�genes de entrada.
        ref_images (ndarray, optional): Las im�genes de referencia. Por defecto es None.
        show_images (int, optional): N�mero de im�genes a mostrar. Por defecto es 5.
        interval (int, optional): Intervalo de �pocas para actualizar las im�genes. Por defecto es 1.
        draw_input (bool, optional): Si se deben dibujar las im�genes de entrada. Por defecto es False.
        fig_size (tuple, optional): Tama�o de la figura. Si es None, se calcula autom�ticamente. Por defecto es None.
    """
    def __init__(self, model, in_images, ref_images=None, show_images=5, interval=1, draw_input=False, fig_size=None):
        super(ImageVisualizer, self).__init__()
        plt.ioff()
        self.model = model
        self.images = in_images
        self.ref_images = ref_images
        self.show_images = show_images
        self.interval = interval
        self.draw_input = draw_input

        (num_rows, num_cols) = (1 + draw_input + (ref_images is not None)*1, show_images)
        if fig_size is None:      
            fig_size = (num_cols * 2.5, num_rows * 3)

        self.fig, self.ax = plt.subplots(num_rows, num_cols, figsize=fig_size, squeeze=False)

        self.display_obj = display.display(display.HTML(''), display_id = True)
       

    def _update_output(self):
        # Guarda el gr�fico en un b�fer de memoria
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png')
        buf.seek(0)

        # Codifica el gr�fico en base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        data = {'image/png': image_base64}
        # Actualizar el gr�fico
        display.update_display(data, raw=True, display_id=self.display_obj.display_id)
    
    def _plot_image(self, ax, title, img):
        """
        Dibuja una imagen en un eje espec�fico.

        Parameters:
            ax (Axes): El eje en el que se dibujar� la imagen.
            title (str): El t�tulo de la imagen.
            img (ndarray): La imagen a dibujar.
        """ 
        
        cmap = 'gray' if img.shape[-1] == 1 else None
        
        # Normalizar imagen original
        img = img.squeeze()
        if img.max() > 1: 
            img = img / 255.0
        
        ax.imshow(img, cmap=cmap)
        ax.set_title(title)
        ax.axis('off')
                    
    def on_epoch_end(self, epoch, logs=None):
        if epoch % self.interval == 0:
            output_row =  1 if self.draw_input else 0
            refer_row = output_row +1
            rnd_idx = random.sample(range(len(self.images)), self.show_images) 
            inp_imgs = self.images[rnd_idx]
            ref_imgs = self.ref_images[rnd_idx]
            # 
            output_imgs = self.model.predict(inp_imgs, verbose=False)
            
            for i in range(self.show_images):
 
                if self.draw_input:
                    self._plot_image(self.ax[0, i], 'Input', inp_imgs[i])
                   
                # mostrar imagen de salida    
                self._plot_image(self.ax[output_row, i], 'Output', output_imgs[i])

                if self.ref_images is not None:
                    self._plot_image(self.ax[refer_row, i], 'Reference', ref_imgs[i])

            # Agregar t�tulo general con el n�mero de �poca
            title_parts = [f"�poca {epoch}"]

            for metric, value in logs.items():
                if metric != 'batch' and metric != 'size':  # Excluir m�tricas no deseadas
                    title_parts.append(f"{metric.capitalize()}: {value:.4f}")

            self.fig.text(0.5, 0.05, " - ".join(title_parts), ha='center', va='bottom', fontsize=14,
                          bbox=dict(facecolor='white', edgecolor='none', pad=5, alpha=1.0)
                         )
            self._update_output()

    def on_train_end(self, logs=None):
        plt.close()
