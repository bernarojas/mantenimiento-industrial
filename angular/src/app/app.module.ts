
import { RouterModule, Routes, Router } from '@angular/router';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms'

//Servicio
import { EquipoService } from './equipo.service'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { CabeceraComponent } from './cabecera/cabecera.component';
import { FooterComponent } from './footer/footer.component';
import { ContactoComponent } from './contacto/contacto.component';
import { InicioComponent } from './inicio/inicio.component';
import { NosotrosComponent } from './nosotros/nosotros.component';
import { EquipoComponent } from './equipo/equipo.component';

const routes: Routes = [
  { path: 'contacto', component: ContactoComponent },
  { path: 'equipo/:id', component: EquipoComponent },
  { path: 'nosotros', component: NosotrosComponent },
  { path: '', component: InicioComponent, pathMatch: 'full' },
  { path: '**', redirectTo: '/', pathMatch: 'full' }
];

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    CabeceraComponent,
    FooterComponent,
    ContactoComponent,
    InicioComponent,
    NosotrosComponent,
    EquipoComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot(routes),
    HttpClientModule,
    FormsModule
  ],
  providers: [EquipoService],
  bootstrap: [AppComponent]
})
export class AppModule { }
