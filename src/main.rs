use eframe::egui;

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
            //ui.label(format!("Hello '{}', age {}", self.name, self.age));    
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
