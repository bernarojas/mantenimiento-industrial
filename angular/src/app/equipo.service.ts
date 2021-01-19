import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Personajes } from './dataservice/datos'
import { ConditionalExpr } from '@angular/compiler';
import { request } from 'http';



@Injectable({
  providedIn: 'root'
})


export class EquipoService {


  constructor(public http: HttpClient) {
  }

  private headers = new Headers({'Content-Type': 'application/json'});
  
  consultar_personas(){ 
    return this.http.get('http://localhost:8000/api/predecirFotos/');
  }

  agregar_personas(data:any){
    return this.http.post('http://localhost:8000/api/predecirFotos/', data);
  }

  eliminar_personas(data: string){
    return this.http.delete(`http://localhost:8000/api/predecirFotos/${data}/`);
  }

  consultar_personas2(){ 

    return this.http.get('http://localhost:8000/apa/predecirFotos/');
  }

  agregar_personas2(data:any): Observable<any>{ 
    return this.http.post<any>('http://localhost:8000/apa/guardar/predecirFotos/', data);
  }

//{headers: this.headers}
}