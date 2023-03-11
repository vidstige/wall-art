use egui;
use egui::{Frame, Pos2, pos2, vec2, Rect, Stroke, Color32};
use egui::epaint;
use egui::emath;

struct LatticeStudio {
}

impl Default for LatticeStudio {
    fn default() -> Self {
        Self {
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
    
                let desired_size = ui.available_width() * vec2(1.0, 0.35);
                let (_id, rect) = ui.allocate_space(desired_size);
    
                let to_screen =
                    emath::RectTransform::from_to(Rect::from_x_y_ranges(0.0..=1.0, -1.0..=1.0), rect);
    
                let mut shapes = vec![];
    
                for &mode in &[2, 3, 5] {
                    let mode = mode as f64;
                    let n = 120;
                    let speed = 1.5;
    
                    let points: Vec<Pos2> = (0..=n)
                        .map(|i| {
                            let t = i as f64 / (n as f64);
                            let amp = (time * speed * mode).sin() / mode;
                            let y = amp * (t * std::f64::consts::TAU / 2.0 * mode).sin();
                            to_screen * pos2(t as f32, y as f32)
                        })
                        .collect();
    
                    let thickness = 10.0 / mode as f32;
                    shapes.push(epaint::Shape::line(points, Stroke::new(thickness, color)));
                }
    
                ui.painter().extend(shapes);
            });
        });
    }
}


fn main() -> Result<(), eframe::Error> {
    // Log to stdout (if you run with `RUST_LOG=debug`).
    //tracing_subscriber::fmt::init();

    let options = eframe::NativeOptions {
        initial_window_size: Some(egui::vec2(320.0, 240.0)),
        ..Default::default()
    };
    eframe::run_native(
        "Lattice Studio",
        options,
        Box::new(|_cc| Box::new(LatticeStudio::default())),
    )
}
