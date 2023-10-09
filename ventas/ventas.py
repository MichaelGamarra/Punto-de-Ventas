from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup



inventario = [ 
    {'codigo':'111','nombre':'Leche', 'precio':10.0, 'cantidad':5},
    {'codigo':'112','nombre':'Yogur', 'precio':8.0, 'cantidad':7}, 
    {'codigo':'113','nombre':'Queso', 'precio':15.0, 'cantidad':3}, 
    {'codigo':'114','nombre':'Mantequilla', 'precio':12.0, 'cantidad':6}, 
    {'codigo':'115','nombre':'Crema', 'precio':9.0, 'cantidad':4}, 
    {'codigo':'116','nombre':'Helado', 'precio':20.0, 'cantidad':2}, 
    {'codigo':'117','nombre':'Nata', 'precio':7.0, 'cantidad':8}, 
    {'codigo':'118','nombre':'Leche condensada', 'precio':14.0, 'cantidad':5}, 
    {'codigo':'119','nombre':'Leche de almendras', 'precio':11.0, 'cantidad':9}, 
    {'codigo':'120','nombre':'Leche de coco', 'precio':13.0, 'cantidad':7}, 
    {'codigo':'121','nombre':'Leche de soja', 'precio':10.0, 'cantidad':6} 
] 



class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last  = BooleanProperty(True)


class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad_carrito'])
        self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))
        self.ids['_precio'].text = str("{:.2f}".format(data['precio_total']))
        return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado']= True
        else:
            rv.data[index]['seleccionado']= False






class SelectableBoxLayoutPopup(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_codigo'].text = data['codigo']
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
        return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(
            rv, index, data)



    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)




    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado']= True
        else:
            rv.data[index]['seleccionado']= False





class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.modificar_producto= None
    
    def agregar_articulo(self,articulo):
        articulo['seleccionado'] = False
        indice = -1
        if self.data:
            for i in range(len(self.data)):
                if articulo['codigo']==self.data[i]['codigo']:
                    indice = i
            if indice >= 0:
                self.data[indice]['cantidad_carrito']+=1
                self.data[indice]['precio_total']=self.data[indice]['precio']*self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                self.data.append(articulo)
        else:
            self.data.append(articulo)

    def eliminar_articulo(self):
        indice=self.articulo_seleccionado()
        precio=0
        if indice >=0:
            self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            precio= self.data[indice]['precio_total']
            self.data.pop(indice)
            self.refresh_from_data()
        return precio

    def articulo_seleccionado(self):
        indice = -1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice = i
                break
        return indice

    def modificar_articulo(self):
        indice=self.articulo_seleccionado()
        if indice >=0:
            popup=CambiarCantidadPopup(self.data[indice],self.actualizar_articulo)
            popup.open()


    def actualizar_articulo(self,valor):
        indice= self.articulo_seleccionado()
        if indice >=0:
            if valor==0:
                self.data.pop(indice)
                self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            else:
                self.data[indice]['cantidad_carrito']=valor
                self.data[indice]['precio_total']=self.data[indice]['precio']*valor
            self.refresh_from_data()
            nuevo_total= 0
            for data in self.data:
                nuevo_total+= data['precio_total']
            self.modificar_producto(False, nuevo_total)


class CambiarCantidadPopup(Popup):
    def __init__(self, data, actualizar_articulo_callback,**kwargs):
        super(CambiarCantidadPopup, self).__init__(**kwargs)
        self.data = data
        self.actualizar_articulo=actualizar_articulo_callback
        self.ids.info_nueva_cantidad_1.text = "Producto: " + self.data['nombre'].capitalize()
        self.ids.info_nueva_cantidad_2.text = "Cantidad: " + str(self.data['cantidad_carrito'])
    

    def validar_input(self,texto_input):
        try:
            nueva_cantidad = int(texto_input)
            self.ids.notificacion_no_valido.text= ' '
            self.actualizar_articulo(nueva_cantidad)
            self.dismiss()
        except:
            self.ids.notificacion_no_valido.text= 'Cantidad no Valida'


class PagarPopup(Popup):
    def __init__(self, total, **kwargs):
        super(PagarPopup, self).__init__(**kwargs)
        self.total=total
        self.ids.total.text= "{:.2f}".format(self.total)

    def mostrar_cambio(self):
        recibido= self.ids.recibido.text
        try:
            cambio= float(recibido).float(self.total)
            if cambio >= 0:
                self.ids.cambio.text=  "{:.2f}".format(cambio)
                self.ids.boton_pagar.disabled= False
            else:
                self.ids.cambio.text= "Pago menor a la cantidad a Pagar"
        except:
            self.ids.cambio.text= "Pago no valido"




class ProductoPorNombrePopup(Popup):
    def __init__(self,input_nombre, agregar_producto_callback,**kwargs):
        super(ProductoPorNombrePopup, self).__init__(**kwargs)
        self.input_nombre = input_nombre
        self.agregar_producto = agregar_producto_callback
    


    def mostrar_articulos(self):
        self.open()
        for nombre in inventario:
            if nombre['nombre'].lower().find(self.input_nombre)>=0:
                producto = {'codigo':nombre['codigo'], 'nombre': nombre['nombre'], 'precio': nombre['precio'],'cantidad': nombre['cantidad']}
                self.ids.rvs.agregar_articulo(producto)

    def seleccionar_articulo(self):
        indice=self.ids.rvs.articulo_seleccionado()
        if indice >= 0:
            _articulo=self.ids.rvs.data[indice]
            articulo={}
            articulo['codigo']= _articulo['codigo']
            articulo['nombre']= _articulo['nombre']
            articulo['precio']= _articulo['precio']
            articulo['cantidad_carrito']= 1
            articulo['cantidad_inventario']= _articulo['cantidad']
            articulo['precio_total']= _articulo['precio']
            if callable(self.agregar_producto):
                self.agregar_producto(articulo)
            self.dismiss()




class VentasWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total= 0.0
        self.ids.rvs.modificar_producto = self.modificar_producto

    def admin(self):
        print("Admin   Presionado")
    
    def signout(self):
        print("signout   git Presionado")

    def eliminar_producto(self):
        menos_precio=self.ids.rvs.eliminar_articulo()
        self.total-=menos_precio
        self.ids.sub_total.text ='$ '+"{:.2f}".format(self.total)

    def modificar_producto(self, cambio= True, nuevo_total= None):
        if cambio:
            self.ids.rvs.modificar_articulo()
        else:
            self.total=nuevo_total
            self.ids.sub_total.text='$ '+"{:.2f}".format(self.total)


    def agregar_producto_codigo(self, codigo):
        for producto in inventario:
            if codigo == producto['codigo']:
                articulo={}
                articulo['codigo']= producto['codigo']
                articulo['nombre']= producto['nombre']
                articulo['precio']= producto['precio']
                articulo['cantidad_carrito']= 1
                articulo['cantidad_inventario']= producto['cantidad']
                articulo['precio_total']= producto['precio']
                self.agregar_producto(articulo)
                self.ids.buscar_codigo.text=''
                break


    def agregar_producto(self,articulo):
        self.total+=articulo['precio']
        self.ids.sub_total.text='$ '+"{:.2f}".format(self.total)
        self.ids.rvs.agregar_articulo(articulo)


    def agregar_producto_nombre(self, nombre):
        self.ids.buscar_nombre.text=' '
        popup=ProductoPorNombrePopup(nombre,self.agregar_producto)
        popup.mostrar_articulos()

    def pagar(self):
        if self.ids.rvs.data:
            popup=PagarPopup(self.total)
            popup.open()
        else:
            self.ids.notificacion_falla.tex='No hay Nada Que Pagar'

    def  nueva_compra(self):
        print('Nueva Compra')



class VentasApp(App):
    def build(self):
        return VentasWindow()
    

if __name__=='__main__':
    VentasApp().run()