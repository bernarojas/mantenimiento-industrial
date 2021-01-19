import { Component, OnInit } from '@angular/core';
import { EquipoService } from './../equipo.service'
@Component({
  selector: 'app-contacto',
  templateUrl: './contacto.component.html',
  styleUrls: ['./contacto.component.css']
})
export class ContactoComponent implements OnInit {
  title:string = "";
  description:string = "";

  personajes:any[] = [];

  personajesEliminar: any[] = [];

  constructor(private _personajes: EquipoService) {}

  guardar_personas(){

    const datos:any = {
      "title": this.title,
      "description": this.description
    }

    this._personajes.agregar_personas2(datos).subscribe((data:any[]) => {
        console.log(data)
        console.log("esta guardando...")
        //alert("Aquí estoy");
        //alert(data);
        this.obtener_personas2()
        },
          error => {
              console.log("Error", error);
              alert("error al crear persona");
          }
        );
  }



  limpiar_datos(){
    this.title = ""
    this.description = ""
  }

  eliminar_personas(item2: any){

    //const datos:number = item2.id
    //alert(datos);
    this._personajes.eliminar_personas(item2.id).subscribe(() => {
      this.obtener_personas2();
    }
    );
    
  }

  obtener_personas2(){
    this._personajes.consultar_personas2().subscribe((data:any[]) => {
          this.personajes = data
        },
        error => {
          console.log("Error", error);
          alert("Error al consultar personas");
        }
      );
  }

  ngOnInit() {
    this.obtener_personas2()
  }

}


