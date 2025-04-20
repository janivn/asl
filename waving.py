import cv2
import mediapipe as mp
import numpy as np
import imageio
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark, NormalizedLandmarkList

# Setup MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Create a black canvas
def create_blank_image():
    return np.zeros((480, 640, 3), dtype=np.uint8)

# Simulated hand landmarks
def generate_dummy_landmarks(position_shift):
    landmarks = []
    for i in range(21):
        x = 0.3 + 0.01 * i + position_shift[0]
        y = 0.3 + 0.005 * i + position_shift[1]
        landmarks.append(NormalizedLandmark(x=x, y=y, z=0))
    return landmarks

# Create simulated frames
def generate_sign_frames(label):
    frames = []
    for i in range(10):
        image = create_blank_image()
        shift = (i * 0.01, i * 0.005) if label == "Hello" else (-i * 0.005, i * 0.005)
        hand_landmarks = generate_dummy_landmarks(shift)

        hand_landmark_proto = NormalizedLandmarkList(landmark=hand_landmarks)
        mp_drawing.draw_landmarks(image, hand_landmark_proto, mp_hands.HAND_CONNECTIONS)

        # Add label text
        cv2.putText(image, f"Sign: {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        frames.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return frames

# Generate both signs
hello_frames = generate_sign_frames("Hello")
welcome_frames = generate_sign_frames("Welcome")

# Combine and save as GIF
all_frames = hello_frames + welcome_frames
imageio.mimsave("hello_welcome.gif", all_frames, fps=5)

print("GIF saved as 'hello_welcome.gif'")




  <!-- Features Section -->
  <section id="features" class="features">
    <div class="container">
      <div class="text-center mb-5">
        <h2>Key Features</h2>
        <p class="text-muted">What makes ASL2Text the best choice for sign language translation</p>
      </div>
      
      <div class="row g-4">
        <div class="col-lg-4 col-md-6">
          <div class="feature-box">
            <div class="feature-icon">
              <i class="bi bi-lightning"></i>
            </div>
            <h4>Real-time Translation</h4>
            <p>Our advanced AI instantly processes sign language gestures and converts them to text in real-time.</p>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="feature-box">
            <div class="feature-icon">
              <i class="bi bi-arrow-repeat"></i>
            </div>
            <h4>Continuous Learning</h4>
            <p>Our system continuously improves through machine learning, adapting to new signs and regional variations.</p>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="feature-box">
            <div class="feature-icon">
              <i class="bi bi-globe"></i>
            </div>
            <h4>Multi-dialect Support</h4>
            <p>ASL2Text supports various ASL dialects and regional sign language variations.</p>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="feature-box">
            <div class="feature-icon">
              <i class="bi bi-phone"></i>
            </div>
            <h4>Mobile Friendly</h4>
            <p>Use ASL2Text on any device with a camera, including smartphones and tablets.</p>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="feature-box">
            <div class="feature-icon">
              <i class="bi bi-shield-check"></i>
            </div>
            <h4>Privacy First</h4>
            <p>Your video data is processed locally when possible and never stored permanently.</p>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="feature-box">
            <div class="feature-icon">
              <i class="bi bi-mic"></i>
            </div>
            <h4>Speech Synthesis</h4>
            <p>Convert ASL translations to spoken words for full communication bridge.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- How It Works -->
  <section id="how-it-works" class="how-it-works">
    <div class="container">
      <div class="text-center mb-5">
        <h2>How ASL2Text Works</h2>
        <p class="text-muted">Our advanced AI technology breaks down the translation process</p>
      </div>
      
      <div class="row align-items-center">
        <div class="col-lg-6">
          <div class="step">
            <div class="step-number">1</div>
            <h4>Hand Detection</h4>
            <p>Our AI identifies and tracks hand movements in the video feed with high precision.</p>
          </div>
          
          <div class="step">
            <div class="step-number">2</div>
            <h4>Gesture Recognition</h4>
            <p>The system analyzes hand shapes, positions, and movements to identify specific signs.</p>
          </div>
          
          <div class="step">
            <div class="step-number">3</div>
            <h4>Context Understanding</h4>
            <p>ASL2Text understands signing context to improve accuracy and manage grammar differences.</p>
          </div>
          
          <div class="step">
            <div class="step-number">4</div>
            <h4>Text Conversion</h4>
            <p>The recognized signs are converted to natural, readable text in real-time.</p>
          </div>
        </div>
        
        <div class="col-lg-6">
          <img src="/api/placeholder/600/500" alt="How ASL2Text Works" class="img-fluid rounded">
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials -->
  <section id="testimonials" class="testimonials">
    <div class="container">
      <div class="text-center mb-5">
        <h2>What Users Say</h2>
        <p class="text-muted">Real experiences from people in the deaf and hearing communities</p>
      </div>
      
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="testimonial-card">
            <div class="stars mb-3">
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
            </div>
            <p>"ASL2Text has revolutionized how I communicate with hearing colleagues. The accuracy is impressive, and it keeps getting better."</p>
            <div class="testimonial-person">
              <div class="testimonial-img">
                <img src="/api/placeholder/50/50" alt="User">
              </div>
              <div>
                <h5 class="mb-0">Sarah Johnson</h5>
                <small class="text-muted">ASL Teacher</small>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4">
          <div class="testimonial-card">
            <div class="stars mb-3">
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
            </div>
            <p>"As a business owner, ASL2Text has helped me make my store more accessible. My deaf customers appreciate being able to communicate easily."</p>
            <div class="testimonial-person">
              <div class="testimonial-img">
                <img src="/api/placeholder/50/50" alt="User">
              </div>
              <div>
                <h5 class="mb-0">Michael Roberts</h5>
                <small class="text-muted">Small Business Owner</small>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4">
          <div class="testimonial-card">
            <div class="stars mb-3">
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-fill text-warning"></i>
              <i class="bi bi-star-half text-warning"></i>
            </div>
            <p>"I've been using ASL2Text in my classroom to help integrate deaf and hearing students. It's become an invaluable educational tool."</p>
            <div class="testimonial-person">
              <div class="testimonial-img">
                <img src="/api/placeholder/50/50" alt="User">
              </div>
              <div>
                <h5 class="mb-0">Elena Torres</h5>
                <small class="text-muted">Special Education Teacher</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Pricing -->
  <section id="pricing" class="pricing">
    <div class="container">
      <div class="text-center mb-5">
        <h2>Simple, Transparent Pricing</h2>
        <p class="text-muted">Choose the plan that fits your needs</p>
      </div>
      
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="pricing-card">
            <h3>Basic</h3>
            <p class="text-muted">For personal use</p>
            <div class="price">Free</div>
            <p class="text-muted">Limited features</p>
            <ul class="pricing-list">
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> Real-time ASL translation</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> 10 translations per day</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> Basic ASL dictionary</li>
              <li><i class="bi bi-x-circle-fill text-danger me-2"></i> Translation history</li>
              <li><i class="bi bi-x-circle-fill text-danger me-2"></i> Video uploads</li>
            </ul>
            <a href="#" class="btn btn-outline-primary w-100">Get Started</a>
          </div>
        </div>
        
        <div class="col-lg-4">
          <div class="pricing-card featured">
            <h3>Pro</h3>
            <p class="text-muted">For individuals</p>
            <div class="price">$9.99</div>
            <p class="text-muted">Per month</p>
            <ul class="pricing-list">
              <li><i class="bi bi-check-circle-fill me-2"></i> Unlimited translations</li>
              <li><i class="bi bi-check-circle-fill me-2"></i> Full ASL dictionary</li>
              <li><i class="bi bi-check-circle-fill me-2"></i> Translation history</li>
              <li><i class="bi bi-check-circle-fill me-2"></i> Video uploads</li>
              <li><i class="bi bi-x-circle-fill opacity-50 me-2"></i> API access</li>
            </ul>
            <a href="#" class="btn btn-light w-100">Start 7-Day Trial</a>
          </div>
        </div>
        
        <div class="col-lg-4">
          <div class="pricing-card">
            <h3>Enterprise</h3>
            <p class="text-muted">For businesses</p>
            <div class="price">$49.99</div>
            <p class="text-muted">Per month</p>
            <ul class="pricing-list">
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> Everything in Pro</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> API access</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> Multiple user accounts</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> Custom integration</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i> Priority support</li>
            </ul>
            <a href="#" class="btn btn-outline-primary w-100">Contact Sales</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Section -->
  <section id="faq" class="faq py-5">
    <div class="container">
      <div class="text-center mb-5">
        <h2>Frequently Asked Questions</h2>
        <p class="text-muted">Find answers to common questions about ASL2Text</p>
      </div>
      
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="accordion" id="faqAccordion">
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">
                  How accurate is ASL2Text?
                </button>
              </h2>
              <div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  ASL2Text currently achieves around 92% accuracy for common signs and phrases in good lighting conditions. Our system is constantly learning and improving through machine learning algorithms and user feedback.
                </div>
              </div>
            </div>
            
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq2">
                  What equipment do I need to use ASL2Text?
                </button>
              </h2>
              <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  You only need a device with a camera and internet connection. ASL2Text works on computers, tablets, and smartphones. For best results, we recommend using a device with a front-facing camera in a well-lit environment.
                </div>
              </div>
            </div>
            
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq3">
                  Does ASL2Text work offline?
                </button>
              </h2>
              <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  Currently, ASL2Text requires an internet connection for full functionality. However, our Pro and Enterprise plans include a limited offline mode that can recognize basic signs without an internet connection.
                </div>
              </div>
            </div>
            
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq4">
                  Can ASL2Text translate other sign languages?
                </button>
              </h2>
              <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  Currently, ASL2Text is focused on American Sign Language (ASL). We're actively developing support for other sign languages including British Sign Language (BSL), Auslan, and more. Sign up for our newsletter to be notified when new languages are available.
                </div>
              </div>
            </div>
            
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq5">
                  Is my data secure with ASL2Text?
                </button>
              </h2>
              <div id="faq5" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                  We take privacy very seriously. Your video data is processed in real-time and is not stored permanently on our servers unless you explicitly save a translation. All data is encrypted, and we never share your information with third parties.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta py-5 bg-gradient text-white">
    <div class="container text-center py-4">
      <h2>Start Breaking Communication Barriers Today</h2>
      <p class="mb-4">Join thousands of users who are already bridging the gap between deaf and hearing communities.</p>
      <div class="d-flex justify-content-center gap-3">
        <a href="#translator" class="btn btn-light btn-lg">Try For Free</a>
        <a href="#pricing" class="btn btn-outline-light btn-lg">View Plans</a>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <div class="container">
      <div class="row g-4">
        <div class="col-lg-4">
          <h3>ASL2<span>Text</span></h3>
          <p>Breaking communication barriers between deaf and hearing communities with cutting-edge AI technology.</p>
          <div class="social-links">
            <a href="#"><i class="bi bi-facebook"></i></a>
            <a href="#"><i class="bi bi-twitter"></i></a>
            <a href="#"><i class="bi bi-instagram"></i></a>
            <a href="#"><i class="bi bi-linkedin"></i></a>
            <a href="#"><i class="bi bi-youtube"></i></a>
          </div>
        </div>
        
        <div class="col-lg-2">
          <h5>Company</h5>
          <ul class="footer-links">
            <li><a href="#">About Us</a></li>
            <li><a href="#">Careers</a></li>
            <li><a href="#">Press</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </div>
        
        <div class="col-lg-2">
          <h5>Product</h5>
          <ul class="footer-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="#">API</a></li>
            <li><a href="#">Integrations</a></li>
            <li><a href="#">Updates</a></li>
          </ul>
        </div>
        
        <div class="col-lg-2">
          <h5>Resources</h5>
          <ul class="footer-links">
            <li><a href="#">Documentation</a></li>
            <li><a href="#">Tutorials</a></li>
            <li><a href="#">Community</a></li>
            <li><a href="#">ASL Dictionary</a></li>
            <li><a href="#">Support</a></li>
          </ul>
        </div>
        
        <div class="col-lg-2">
          <h5>Legal</h5>
          <ul class="footer-links">
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Accessibility</a></li>
            <li><a href="#">GDPR</a></li>
            <li><a href="#">Cookie Policy</a></li>
          </ul>
        </div>
      </div>
      
      <div class="copyright">
        <p>&copy; 2025 ASL2Text. All rights reserved.</p>
      </div>
    </div>
  </footer>
