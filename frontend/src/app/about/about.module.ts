import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AboutComponent } from './about/about.component';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '**',
    pathMatch: 'full',
    component: AboutComponent,
  },
];

@NgModule({
  declarations: [AboutComponent],
  imports: [RouterModule.forChild(routes), CommonModule],
})
export class AboutModule {}
