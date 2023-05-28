import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartViewComponent } from './chart-view/chart-view.component';
import { ChartComponent } from './chart/chart.component';
import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


const routes: Routes = [
  {
    path: '**',
    pathMatch: 'full',
    component: ChartViewComponent,
  },
];

@NgModule({
  declarations: [ChartViewComponent, ChartComponent],
  imports: [
    RouterModule.forChild(routes), FormsModule, CommonModule, HttpClientModule
  ],
})
export class ChartViewModule { }
