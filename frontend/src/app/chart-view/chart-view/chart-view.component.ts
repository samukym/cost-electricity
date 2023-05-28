import { Component } from '@angular/core';
import { ChartViewService, CostSlot } from '../chart-view.service';

@Component({
  selector: 'app-chart-view',
  templateUrl: './chart-view.component.html',
  styleUrls: ['./chart-view.component.css'],
  providers: [ChartViewService]
})

export class ChartViewComponent {
  sensorIds: Array<string> = [];
  consumeCost: Array<CostSlot> = []
  selectedOption: any = "";

  constructor(private chartViewService: ChartViewService) { }

  ngOnInit() {
    this.chartViewService.getSensors().subscribe(
      sensorIds => {
        this.sensorIds = sensorIds
        this.selectedOption = this.sensorIds[0]
        this.fetchConsumeForSensor(this.selectedOption)
      },
      error => console.error(error)
    );
  }

  onSelectionChange() {
    this.fetchConsumeForSensor(this.selectedOption)
  }

  private fetchConsumeForSensor(sensorId: string) {
    this.chartViewService.getCostConsumeForSensor(sensorId)
      .subscribe(consume => this.consumeCost = consume)
  }
}
