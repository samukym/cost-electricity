import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';

export interface CostSlot {
  timestamp: Date
  cost: number
}

interface CostSlotRaw {
  timestamp: number
  cost: number
}

@Injectable({
  providedIn: 'root'
})

export class ChartViewService {
  private readonly baseAPIUrl = "http://localhost:5000";

  constructor(private http: HttpClient) { }

  getSensors(): Observable<Array<string>> {
    return this.http.get<Array<string>>(this.baseAPIUrl + '/sensors');
  }

  getCostConsumeForSensor(sensorId: string): Observable<Array<CostSlot>> {
    return this.http.get<Array<CostSlotRaw>>(this.baseAPIUrl + `/sensors/${sensorId}`)
      .pipe(
        map((costSlots: Array<CostSlotRaw>) => {
          return costSlots.map((costSlot: CostSlotRaw) => ({ 
            cost: costSlot.cost, timestamp: new Date(costSlot.timestamp * 1000) 
          }))
        })
      )
  }
}
