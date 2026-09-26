export type RouteGeometry = Record<string, [number, number][]>;

export interface OptimizationResponse {
  success?: boolean;
  best_time: number;
  distance?: number;
  routes: Record<string, string[]>;
  route_geometry: RouteGeometry;
  output?: string;
  error?: string;
}

export const optimizeRoutes = async (incident: boolean = false): Promise<OptimizationResponse> => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/optimize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // Pass the incident state to FastAPI
      body: JSON.stringify({ incident }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: OptimizationResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to execute QPSO optimization:", error);
    throw error;
  }
};
export const triggerTrafficIncident = async (): Promise<OptimizationResponse> => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/incident", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: OptimizationResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to execute traffic incident re-optimization:", error);
    throw error;
  }
};