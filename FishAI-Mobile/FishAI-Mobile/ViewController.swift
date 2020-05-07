//
//  ViewController.swift
//  FishAI-Mobile
//
//  Created by Alvin H Lai on 2020-05-06.
//  Copyright © 2020 Alvin H Lai. All rights reserved.
//

import UIKit
import Vision
import AVFoundation


class ViewController: UIViewController {
    
    // turn off the top panel (battery stuff)
    
    @IBOutlet weak var cameraView: UIView!
    @IBOutlet weak var tmpImage: UIImageView!
    @IBOutlet weak var resultLabel: UILabel!
    @IBOutlet weak var resultView: UIView!
    
    var captureSession: AVCaptureSession!
    var previewVideoLayer: AVCaptureVideoPreviewLayer!
    
    func hideResults(){
        self.resultView.alpha = 0;
    }
    
    func showResults(){
        self.resultView.alpha = 1;
    }
    
    lazy var vnRequest: VNCoreMLRequest = {
        let vnModel = try! VNCoreMLModel(for: FishAI_Model().model)
        let request = VNCoreMLRequest(model: vnModel) { [unowned self] request , _ in
            self.processingResult(for: request)
        }
        request.imageCropAndScaleOption = .centerCrop // we need to make it the same size (244,244,3)
        return request
    }()
    
    func classify(image: UIImage) {
        DispatchQueue.global(qos: .userInitiated).async {
            let ciImage = CIImage(image: image)!
            let imageOrientation = CGImagePropertyOrientation(rawValue: UInt32(image.imageOrientation.rawValue))!
            let handler = VNImageRequestHandler(ciImage: ciImage, orientation: imageOrientation)
            try! handler.perform([self.vnRequest])
        }
    }
    
    func processingResult(for request: VNRequest){
        DispatchQueue.main.async {
            let results = (request.results! as! [VNClassificationObservation]).prefix(2)
            guard let observation = results.first else {return}
            self.resultLabel.text = observation.identifier
            self.showResults()
        }
    }
    
    
}

