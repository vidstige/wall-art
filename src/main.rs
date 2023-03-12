use egui;
use egui::{Frame, Pos2, Rect, Stroke, Color32};
use egui::{pos2};
use egui::epaint;
use egui::emath;

struct LatticeStudio {
    points: Vec<Pos2>,
    edges: Vec<(usize, usize)>,
}

fn idx(x: usize, y: usize, w: usize) -> usize{
    y * w + x
}

impl LatticeStudio {
    fn new() -> Self {
        Self {
            points: Vec::new(),
            edges: Vec::new(),
        }
    }

    fn euclidian(&mut self) {
        // add points
        let n = 10;
        for x in 0..n {
            for y in 0..n {
                self.points.push(pos2(x as f32 / n as f32, y as f32 / n as f32));
            }
        }
        // add vertices
        for x in 0..n-1 {
            for y in 0..n-1 {
                self.edges.push((idx(x, y, n), idx(x + 1, y, n)));
                self.edges.push((idx(x, y, n), idx(x, y + 1, n)));
                self.edges.push((idx(x + 1, y, n), idx(x, y + 1, n)));
            }
        }
    }
}

impl eframe::App for LatticeStudio {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("Lattice Studio");
            if ui.button("Abc").clicked() {
                
            }
            let color = Color32::from_additive_luminance(196);
            Frame::canvas(ui.style()).show(ui, |ui| {
                ui.ctx().request_repaint();
                let time = ui.input(|i| i.time);
    
                let desired_size = ui.available_size();
                let (_id, rect) = ui.allocate_space(desired_size);
    
                let to_screen =
                    emath::RectTransform::from_to(Rect::from_x_y_ranges(0.0..=1.0, 0.0..=1.0), rect);
    
                let thickness = 2.0;
                let mut shapes = vec![];
                for (i0, i1) in self.edges.iter() {
                    let points = [to_screen * self.points[*i0], to_screen * self.points[*i1]];
                    shapes.push(epaint::Shape::line(points.to_vec(), Stroke::new(thickness, color)));
                }
                ui.painter().extend(shapes);
            });
        });
    }
}

fn create_app() -> LatticeStudio {
    let mut app = LatticeStudio::new();
    app.euclidian();
    return app;
}

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        initial_window_size: Some(egui::vec2(320.0, 240.0)),
        ..Default::default()
    };
    eframe::run_native(
        "Lattice Studio",
        options,
        Box::new(|_cc| Box::new(create_app())),
    )
}
