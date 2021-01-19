import { Component, OnInit } from '@angular/core';
import { EquipoService } from './../equipo.service'
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-equipo',
  templateUrl: './equipo.component.html',
  styleUrls: ['./equipo.component.css']
})
export class EquipoComponent implements OnInit {

  equipo:any[] = [];
  constructor(){}

  ngOnInit() {
  }

}
