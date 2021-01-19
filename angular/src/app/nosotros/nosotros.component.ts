import { Component, OnInit } from '@angular/core';
import { EquipoService } from './../equipo.service';
import { Observable } from 'rxjs';
import { Config } from 'protractor';
import { Personajes } from './../dataservice/datos';


@Component({
  selector: 'app-nosotros',
  templateUrl: './nosotros.component.html',
  styleUrls: ['./nosotros.component.css']
})
  export class NosotrosComponent implements OnInit {

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

      this._personajes.agregar_personas(datos).subscribe((data:any[]) => {
          console.log(data)
          //alert("Aquí estoy");
          //alert(data);
          this.obtener_personas()
          },
            error => {
                console.log("Error", error);
                alert("error al crear persona");
            }
          );
    }


    obtener_personas(){
      this._personajes.consultar_personas().subscribe((data:any[]) => {
            this.personajes = data
          },
          error => {
            console.log("Error", error);
            alert("Error al consultar personas");
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
        this.obtener_personas();
      }
      );
      
    }


    ngOnInit() {
      this.obtener_personas()
    }
        //eliminar_personas(item2){

    /*  const datos:any = {
        "id": item2.id,
        "title": item2.title,
        "description": item2.description
      }
      alert("eliminando");
      alert(datos.id);
      alert(datos.title);
      alert(datos.description);
      this._personajes.eliminar_personas(datos)
    }*/

  }


